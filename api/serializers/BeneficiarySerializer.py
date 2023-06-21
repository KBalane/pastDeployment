from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from digiinsurance.models.Beneficiaries import Beneficiaries
from digiinsurance.models.TempBeneficiaries import TempBeneficiaries
from digiinsurance.models.InsureePolicy import InsureePolicy


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = '__all__'


class TempBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TempBeneficiaries
        fields = '__all__'


class BeneficiaryInfoSerializer(serializers.Serializer):
    user_policy_id = serializers.IntegerField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    birthday = serializers.DateField()
    birthplace = serializers.CharField()
    country = serializers.CharField()
    nationality = serializers.CharField()
    beneficiary_address = serializers.CharField()
    relationship = serializers.CharField()
    percentage_of_share = serializers.DecimalField(10, 2)
    beneficiary_status = serializers.CharField()
    request_type = serializers.CharField()

    class Meta:
        model = Beneficiaries
        fields = ('id', 'user_policy_id', 'first_name', 'middle_name',
                  'last_name', 'birthday', 'birthplace', 'country', 'nationality',
                  'beneficiary_address', 'relationship', 'percentage_of_share',
                  'beneficiary_status', 'request_type')

    def validate_user_policy_id(self, user_policy_id):
        insureePolicy = InsureePolicy.objects.filter(pk=user_policy_id)
        if not insureePolicy.exists():
            raise serializers.ValidationError(
                _("User policy ID does not exist!"))
        return user_policy_id

    def create(self, validated_data):
        return Beneficiaries.objects.create(**validated_data)
