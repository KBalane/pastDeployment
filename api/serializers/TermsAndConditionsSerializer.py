import base64
import json

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from digiinsurance.models import TermsAndConditions

__all__ = ['UpdateTermsAndCondition']


class UpdateTermsAndCondition(serializers.ModelSerializer):
    
    class Meta:
        model = TermsAndConditions
        fields = '__all__'

