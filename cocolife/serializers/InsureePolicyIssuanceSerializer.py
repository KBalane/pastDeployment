from rest_framework import serializers

from cocolife.models.InsureePolicyIssuanceSettings import *

__all__ = ['InsureePolicyIssuanceSettings']


class InsureePolicyIssuanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsureePolicyIssuanceSettings
        fields = '__all__'
