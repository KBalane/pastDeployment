from rest_framework import serializers

from cocolife.models.DigiTransaction import DigiTransaction

__all__ = ['CLPaymentSerializer', 'CLTransactionSerializer']


class CLPaymentSerializer(serializers.ModelSerializer):
    productInsuree = serializers.IntegerField()
    action = serializers.CharField()

    class Meta:
        model = DigiTransaction
        fields = ('productInsuree','action')


class CLTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigiTransaction
        fields = '__all__'
