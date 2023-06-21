from django.utils.translation import ugettext_lazy as _

from digiinsurance.models.Insuree import Insuree
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.Transaction import Transaction

from rest_framework import serializers


class InsureeSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()

    class Meta:
        model = Insuree
        fields = ('user_id', 'last_name', 'first_name', 'middle_name',
                  'mobile_number', 'email')


class GetInsureeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class InsureePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsureePolicy
        fields = '__all__'


class InsureePolicySerializer2(serializers.ModelSerializer):
    class Meta:
        model = InsureePolicy
        # fields = ('id', 'first_name', 'middle_name', 'last_name')
        fields = '__all__'
