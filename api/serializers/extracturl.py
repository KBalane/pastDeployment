from rest_framework import serializers

__all__ = ['URLSerializer']


class URLSerializer(serializers.Serializer):
    extract_url = serializers.CharField()
