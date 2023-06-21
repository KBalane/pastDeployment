from rest_framework import serializers

from cocolife.models.CompanyInformation import *

__all__ = ["CompanyInformationSerializer"]

class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInformation
        fields = ('__all__')