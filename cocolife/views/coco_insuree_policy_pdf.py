from re import A
from django.db.models.aggregates import Sum
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import Http404

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa

from reportlab.pdfgen import canvas  
from cocolife.models import DigiInsuree

from cocolife.models import PolicyOwner
from cocolife.models.Product import Product,Premium,Benefit
from cocolife.models.ProductInsuree import ProductInsuree
from django.core.serializers.json import json

from datetime import date
import datetime
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.db.models import Q
import pandas as pd
from dateutil.relativedelta import relativedelta

from rest_framework.permissions import AllowAny


__all__ = ['CLGeneratePDF_Policy',]

class CLGeneratePDF_Policy(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id_search,*args, **kwargs):
        try:
            selfinsured = ProductInsuree.objects.all().values_list(  #Query to get self insured if true or false
                'is_self_insured').filter(billed_to_id = id_search).first() 
            #Owner/Payor
            payor = ProductInsuree.objects.all().values_list(
                'billed_to').annotate(name=Concat(
                    'billed_to__first_name',                          #billed_to__first_name
                    V(' '), 'billed_to__last_name', V(''),            #billed_to__last_name
                    output_field=CharField()
                    )).filter(billed_to_id = id_search).first()           
            if selfinsured[0] == True:                             
                insured = payor
            else:  # if not self insured will display policy owner as insured
                #Insured
                insured = PolicyOwner.objects.all().values_list(
                    'insured_by').annotate(name=Concat(
                    'insured_by__first_name',                          
                    V(' '), 'insured_by__last_name', V(''),            
                    output_field=CharField()
                    )).first()
            
            query=ProductInsuree.objects.all().values_list(
               'package__name','coverage_term','variant','created_at','premium_due_date', 'premium_amount_due').filter(billed_to=id_search)
            coco_user_id = DigiInsuree.objects.get(user_id=id_search)
            insurance_plan = query[0][0]                    #Insurance Plan
            coverage_term = query[0][1]                     #Coverage Term
            variant = query[0][2]                           #Variant
            effective_date=query[0][3]                      #Effective Date
            premium_amount_due = query[0][5]                #Amount Due
            premium_due_date = query [0][4]                 #Amount Due Date
            
            expiry_year = effective_date.year + coverage_term                            # Calculation for effective date year
            exp=datetime.date(expiry_year,effective_date.month,effective_date.day)      #MALUPITANG EXPIRATION BY DODO, DAN AT RAPRAP, 2021
            
            # AGE AND MAX AGE in POLICY
            age=coco_user_id.get_age() #GET AGE
            
            # 5 - 17
            # 18 - 45
            # 46 - 55
            # 56 - 64
            #region algo
            if age>=5 and age<=17:
                min=5
                max=17
            elif age>=18 and age<=45:
                min=18
                max=45
            elif age>=46 and age<=55:
                min=46
                max=55
            elif age>=56 and age<=64:
                min=56
                max=64
            else:
                return Response("Age invalid!")
            
            #endregion

            #Max Age & Maximum Renewable Age
            max_age=Premium.objects.all().values('age_max').filter(Q(variant_id=variant) & Q(coverage_term=coverage_term) & Q(age_min=min) & Q(age_max=max))
            renew_age=max-1
            #FACE AMOUNT
            face_amt=Benefit.objects.all().values_list('face_amount').filter(variant_id=variant).order_by('-face_amount')[:1].get()
            
            #benefits=Premium.objects.all().values_list('value','variant').filter(Q(variant_id=variant) & Q(coverage_term=coverage_term) & Q(age_min=min) & Q(age_max=max)).order_by('variant')
            #benefits2=Benefit.objects.all().values_list('face_amount','name').filter(variant_id=variant).order_by('variant')
            #premium = Premium.objects.all().values_list('value','variant').filter(Q(variant_id=variant) & Q(coverage_term=coverage_term) & Q(age_min=min) & Q(age_max=max))
            benefit = Benefit.objects.all().filter(variant_id=variant)
            

            data = {
                'insurance_plan':insurance_plan,
                'coverage_term':coverage_term,
                'max_age':max_age[0]['age_max'],                                
                'payor':payor[1],
                'insured':insured[1],
                'id': insured[0],
                'age':age,
                'effective_date':effective_date,
                'expiry_date':exp,
                'renew_age':renew_age,
                'face_amt':face_amt[0],
                'benefit': benefit,
                'premium': premium_amount_due,
                'premium_due_date': premium_due_date
                }
            
            #PDF GENERATION

            template = get_template('productinsureepdf.html')       #Template from cocolife/templates
            data_p=template.render(data)
            response = BytesIO()
            pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
            if not pdf_page.err:
                #return HttpResponse(response.getvalue(), content_type='application/pdf')
                response = HttpResponse(response.getvalue(), content_type='application/pdf')
                filename = "policy_invoice_%s.pdf" %(id_search)                                     
                content = "inline; filename=%s" %(filename)                                      
                download = request.GET.get("download")
                #if download: #to enable viewing functionality, uncomment this line and indent the next line.
                content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Error Generating PDF")
            return Response(data)
        except TypeError as te:
            raise Http404