from rest_framework import serializers

from cocolife.models import Feature

__all__ = ['FeatureSerializer']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
