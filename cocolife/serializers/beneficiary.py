from rest_framework import serializers
from cocolife.models import Beneficiary

__all__ = ['BeneficiarySerializer']


class BeneficiarySerializer(serializers.ModelSerializer):
    percentage_share = serializers.IntegerField()
    class Meta:
        model = Beneficiary
        fields = ('__all__')
