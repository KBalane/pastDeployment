from digiinsurance.models import Company, BankAccount, UserBankAccount

#from api.serializers import CompanySerializer, BankAccountSerializer, UserBankAccountSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

__all__ = ['Company_Bank_Info']


class Company_Bank_Info(APIView):
    def get(self,request, id_search): 
        permission_classes = (IsAuthenticated, )
        

        provider = BankAccount.objects.values('provider').filter(company__id = id_search)
        branch =  BankAccount.objects.values('branch').filter(company__id = id_search)
        account_number = BankAccount.objects.values('account_number').filter(company__id = id_search)

        context = {
            "bank" : provider,
            "branch" : branch,
            "account_number" : account_number

        }
        return Response(context)


        """
        Choices are: Policies, address, archived, archived_at, 
        area_code, bank_account, city, config, country, country_code,
        cover, created_at, domain, dragonpay_merchant_id, email, gps_lat, 
        gps_long, id, insurance_staff, logo, mobile_number, modified_at, 
        name, payments, phone_number, primary_color, province, region, 
        socials, templates, website, zip_code
        
        name = Claims.objects.all().values('id').annotate(policy_holder=Concat(
                'UserPolicy_id__insuree__first_name',
                V(' '), 'UserPolicy_id__insuree__last_name', V(''),
                output_field=CharField()
                )).filter(UserPolicy_id = id_search)

        user_account_number = Claims.objects.all().values(
            'UserPolicy_id__insuree__user_id'
            ).filter(UserPolicy_id = id_search)

        claim_number = Claims.objects.all().values(
            'id'
        ).filter(UserPolicy_id = id_search)

        policy_type_id = Claims.objects.all().values(
            'UserPolicy_id__policy_type',
            'UserPolicy_id__policy'
        ).filter(UserPolicy_id = id_search)

        claim_completed_date = Claims.objects.all().values(
            'modified_at'
        ).filter(UserPolicy_id = id_search)

        total_payments = Claims.objects.all().values(
            'amount'
        ).filter(UserPolicy_id = id_search).aggregate(total = Sum('amount'))

        claim_status = Claims.objects.all().values(
            'UserPolicy_id__status'
        ).filter(UserPolicy_id = id_search)

        risk_details = Claims.objects.all().values(
            'details'
        ).filter(UserPolicy_id = id_search)
        
        context = {
            "name": name,
            "user_account_num" : user_account_number,
            "claim_number" : claim_number,
            "policy_type_id" : policy_type_id,
            "claim_completed_date" : claim_completed_date,
            "total_payments" : total_payments,
            "claim_status" : claim_status,
            "risk_details" : risk_details
        }
                
        return Response(context)
        """
