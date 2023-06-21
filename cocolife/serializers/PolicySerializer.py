import base64
import json

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from digiinsurance.models import Policy

__all__ = ['PackagesJSONSerializer']

class PackagesJSONSerializer(serializers.ModelSerializer):
    packages = serializers.JSONField()

    class Meta:
        model = Policy
        fields = ('packages',)
