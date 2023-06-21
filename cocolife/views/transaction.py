from rest_framework.generics import ListAPIView

from cocolife.serializers.DigiTransactionSerializer import CLTransactionSerializer
from cocolife.models.DigiTransaction import DigiTransaction


__all__ = ['Transactions']


class Transactions(ListAPIView):
    queryset = DigiTransaction.objects.all()
    serializer_class = CLTransactionSerializer


