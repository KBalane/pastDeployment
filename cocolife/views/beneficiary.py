from cocolife.models import Beneficiary
from cocolife.serializers import BeneficiarySerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

__all__ = ['BeneficiaryByID', 'Beneficiary']


class BeneficiaryByID(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer


class Beneficiary(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

    def get_queryset(self):
        beneficiary = super().get_queryset()
        insuree = self.request.query_params.get('insuree')
        if insuree:
            beneficiary = beneficiary.filter(product_insuree=insuree)
        return beneficiary
