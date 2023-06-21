from digiinsurance.models import Company, BankAccount, UserBankAccount
from api.serializers import CompanySerializer, BankAccountSerializer, UserBankAccountSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

__all__ = ['Company_Details']


class Company_Details(APIView):
    def get(self,request, id_search): 
        permission_classes = (IsAuthenticated, )
        name = Company.objects.values('name').filter(id = id_search)
        created_at = Company.objects.values('created_at').filter(id = id_search)
        BankAccount_account_number = BankAccount.objects.values('account_number').filter(company__id = id_search)
        address = Company.objects.values('id').annotate(full_address=Concat(
                'address',V(', '), 
                'city', V(', '), 
                'province', V(', '), 
                'region', V(', '),
                'zip_code', V(''),
                output_field=CharField()
                )).filter(id = id_search)


        stuff = Company.objects.all().filter(id = id_search)
        serializer = CompanySerializer(stuff,many=True)

        context = {
            "company_name" : name,
            "created_on" : created_at,
            "account_number" : BankAccount_account_number,
            "bank_address" : address

        }
        return Response(context)


        """
        Choices are: Policies, address, archived, archived_at, 
        area_code, bank_account, city, config, country, country_code,
        cover, created_at, domain, dragonpay_merchant_id, email, gps_lat, 
        gps_long, id, insurance_staff, logo, mobile_number, modified_at, 
        name, payments, phone_number, primary_color, province, region, 
        socials, templates, website, zip_code
        """
