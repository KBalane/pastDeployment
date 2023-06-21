from typing import List
from cocolife.serializers import PolicyOwnerSerializer
from cocolife.models import PolicyOwner

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

__all__=['PolicyOwnerbyID','PolicyOwner']

class PolicyOwnerbyID(RetrieveUpdateDestroyAPIView):
    permission_classes=(AllowAny,)
    lookup_field='pk'
    queryset = PolicyOwner.objects.all()
    serializer_class=PolicyOwnerSerializer


class PolicyOwner(ListCreateAPIView):
    permission_classes=(AllowAny,)
    queryset=PolicyOwner.objects.all()
    serializer_class=PolicyOwnerSerializer

    # def get_queryset(self):
    #     po = super().get_queryset()
    #     insured_by = self.request.query_params.get('insured_by_id')
    #     if type:
    #         po = po.filter(insured_by_id=insured_by)
    #     return po