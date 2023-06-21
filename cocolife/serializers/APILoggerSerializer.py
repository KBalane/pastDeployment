from rest_framework import serializers

from cocolife.models.APILogger import APILogger


__all__ = ['APILoggerSerializer']


class APILoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILogger
        fields = ['__all__']
