from rest_framework import serializers

from cocolife.models import APIKey

__all__ = ['APIKeySerializer']


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'
