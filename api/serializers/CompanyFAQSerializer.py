from rest_framework import serializers

from digiinsurance.models.CompanyFAQ import CompanyFAQ


class CompanyFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFAQ
        fields = '__all__'
