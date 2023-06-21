from rest_framework import serializers
from telco.models import (
    TelcoPersonAddress,
    TelcoSimDetails,
    TelcoCompany,
    JumioToken
)


class TelcoPersonAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelcoPersonAddress
        fields = ('__all__')


class TelcoSimDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelcoSimDetails
        fields = ('__all__')


class TelcoCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TelcoCompany
        fields = ('__all__')

class JumioTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumioToken
        fields = ('__all__')
