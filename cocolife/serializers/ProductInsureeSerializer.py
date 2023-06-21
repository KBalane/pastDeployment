from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import is_simple_callable
from cocolife.models.Product import *
from cocolife.models import ProductInsuree

__all__ = ['ProductInsureeSerializer']

class ProductInsureeSerializer(serializers.ModelSerializer):
    payment_term = serializers.CharField()
    coverage_term = serializers.IntegerField()
    class Meta:
        model = ProductInsuree
        fields = ('__all__')
    
    def validate_payment_term(self, value):
        if value not in ['annual', 'semi annual', 'quarterly', 'monthly']:
            raise serializers.ValidationError('Invalid value for Payment Term.')
        return value

    def create(self, validated_data):
        obj = ProductInsuree.objects.create(**validated_data)
        obj.update_due_date()
        return obj

