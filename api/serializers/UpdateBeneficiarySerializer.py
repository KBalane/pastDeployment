from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from digiinsurance.models.Beneficiaries import Beneficiaries
from digiinsurance.models.InsureePolicy import InsureePolicy

__all__ = ['BeneficiaryApproveSerializer', 'BeneficiaryUpdateSerializer',
           'BeneficiaryDeleteSerializer', 'GetBeneficiaryInfoSerilizer', 'BeneficiaryListSerializer',
           'BeneficiaryJSONSerializer', 'BeneficiaryGetPendingUpdates', 'BeneficiaryJSONIDSerializer']


class BeneficiaryUpdateSerializer(serializers.ModelSerializer):
    user_policy_id = serializers.IntegerField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField()
    birthday = serializers.DateField()
    birthplace = serializers.CharField()
    country = serializers.CharField()
    nationality = serializers.CharField()
    beneficiary_address = serializers.CharField()
    relationship = serializers.CharField()
    beneficiary_status = serializers.CharField()
    request_type = serializers.CharField()
    percentage_of_share = serializers.DecimalField(10, 2)

    class Meta:
        model = Beneficiaries
        fields = ('id', 'user_policy_id', 'first_name', 'middle_name',
                  'last_name', 'birthday', 'birthplace', 'country', 'nationality',
                  'beneficiary_address', 'relationship', 'beneficiary_status',
                  'request_type', 'percentage_of_share')

    def validate_user_policy_id(self, user_policy_id):
        insuree_policy = InsureePolicy.objects.filter(pk=user_policy_id)
        if not insuree_policy.exists():
            raise serializers.ValidationError(
                _("User policy ID does not exist!"))
        return user_policy_id


class BeneficiaryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = ('id', 'user_policy_id', 'first_name', 'middle_name',
                  'last_name', 'birthday', 'birthplace', 'country', 'nationality', 'beneficiary_address',
                  'relationship')


class GetBeneficiaryInfoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = '__all__'


class BeneficiaryApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = ('id', 'user_policy_id', 'beneficiary_status')


class BeneficiaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaries
        fields = '__all__'


# refactor changes

class BeneficiaryJSONSerializer(serializers.ModelSerializer):
    update_fields = serializers.JSONField()

    class Meta:
        model = Beneficiaries
        fields = ('update_fields',)


class BeneficiaryJSONIDSerializer(serializers.ModelSerializer):
    update_fields = serializers.JSONField()

    class Meta:
        model = Beneficiaries
        fields = ('id', 'update_fields',)


class BeneficiaryGetPendingUpdates(serializers.ModelSerializer):
    # update_fields = serializers.JSONField()

    class Meta:
        model = Beneficiaries
        fields = ("id", "created_at", "modified_at",
                  "first_name",
                  "middle_name",
                  "last_name",
                  "relationship",
                  "birthday",
                  "birthplace",
                  "nationality",
                  "country",
                  "beneficiary_address",
                  "beneficiary_status",
                  "request_type",
                  "percentage_of_share",
                  "reason")
