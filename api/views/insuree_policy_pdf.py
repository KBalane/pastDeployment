from django.http.response import Http404
from digiinsurance.models import InsureePolicy
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

from django.core.serializers.json import json

from datetime import datetime
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from rest_framework.permissions import AllowAny


__all__ = ['GeneratePDF_Policy',]

class GeneratePDF_Policy(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id_search,*args, **kwargs):
        try:
            policies = InsureePolicy.objects.all().filter(insuree_id = id_search)
            name = InsureePolicy.objects.all().values_list(
                'insuree').annotate(name=Concat(
                    'insuree__first_name',
                    V(' '), 'insuree__last_name', V(''),
                    output_field=CharField()
                    )).filter(insuree_id = id_search).first()
            data = {
                'policies':policies,
                'name':name[1],
                'id':name[0]
                }
            template = get_template('insuree_policy_invoice.html')
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
        except TypeError as te:
            raise Http404