from rest_framework import serializers

from digiinsurance.models.Transaction import Transaction

__all__ = ['GetTransactionHistorySerializer', 'TransactionSerializer', 'PaymentSerializer']


class GetTransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('insuree_id',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "insuree_id": self.request.query_params.get('insuree_id'),
                "start_date": self.request.query_params.get('start_date'),
                "end_date": self.request.query_params.get('end_date')
            }
        )
        return context


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    insureePolicy = serializers.IntegerField()
    action = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ('insureePolicy', 'action')
