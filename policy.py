import base64
import json

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from digiinsurance.models.Policy import Policy

__all__ = ['GetAllPolicySerializer', 'GetPolicyBenefitsSerializer', 'PolicySerializer', 'DownloadPDFPolicySerializer',
           'CreateProductSerializer']


class GetAllPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class GetPolicyBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'packages')


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('company', 'name', 'description', 'packages')


class DownloadPDFPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'adminupload', 'pdfname')


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = '__all__'
