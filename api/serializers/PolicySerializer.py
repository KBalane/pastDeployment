import base64
import json

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from digiinsurance.models.Policy import Policy, PolicyCalculator, PolicyRequirements

__all__ = ['UpdateTermsAndConditionPerPolicy', 'GetAllPolicySerializer',
           'GetPolicyBenefitsSerializer', 'PolicySerializer', 'DownloadPDFPolicySerializer',
           'PolicyImageSerializer', 'UploadPolicySerializer', 'CertificateTemplateSerializer',
           'PolicyCalculatorSerializer', 'CreateProductSerializer', 'PolicyRequirementsSerializer',
           'EditPolicyPackagesSerializer', 'UpdateFileFieldSerializer', 'ViewPolicySerializer']


class PolicyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'icon_name', 'icon_file',)


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
        fields = (
        'company', 'name', 'description', 'packages', 'payment_interval', 'category', 'payment_option', 'question',
        'passing_score', 'benefits_basic', 'benefits_lite', 'benefits_standard', 'benefits_pro')


class ViewPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = (
        'company', 'name', 'description', 'packages', 'payment_interval', 'category', 'payment_option', 'question',
        'passing_score', 'is_recommended')


class EditPolicyPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('packages',)  # 'payment_interval', 'payment_option'


class DownloadPDFPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'adminupload', 'pdfname')


class UploadPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('__all__')


class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'adminupload', 'pdfname')


class PolicyCalculatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCalculator
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class PolicyRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRequirements
        fields = '__all__'


class UpdateTermsAndConditionPerPolicy(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('adminupload',)


class UpdateFileFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('benefits_basic', 'benefits_lite', 'benefits_standard', 'benefits_pro')
