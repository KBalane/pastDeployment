from digiinsurance.models.Company import Company
from digiinsurance.models.BankAccounts import BankAccount
from digiinsurance.models import CompanyRequirements

from rest_framework import serializers


__all__ = [ 'CompanySerializer','BankAccountSerializer', 'CompanyRequirementsSerializer', 'PhotoCompanySerializer']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class CompanyRequirementsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = CompanyRequirements
        fields = '__all__'


class PhotoCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('logo', 'cover')
