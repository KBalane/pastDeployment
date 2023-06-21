from django.db.models import fields
from rest_framework import serializers
from cocolife.models import Underwriting

__all__ = ['UnderwriterSerializer', 'UnderwriterStatusSerializer']


class UnderwriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Underwriting
        fields = '__all__'


class UnderwriterStatusSerializer(serializers.ModelSerializer):
    # underwriting = InsureePolicySerializer(many=True)
    # uuu= UserSerializer(many=True, read_only=True)
    insuree_policy = serializers.CharField()

    # editor = serializers.CharField()
    class Meta:
        model = Underwriting
        fields = ['insuree_policy', 'underwriter_status', 'editor']
