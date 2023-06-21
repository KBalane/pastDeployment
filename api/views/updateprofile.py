from rest_framework import viewsets, generics
from rest_framework.response import Response

from api.serializers import AccountUpdateSerializer
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView

from digiinsurance.models import Insuree
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 

__all__ = ['UpdateProfileDetails','GetSpecificProfile']

class GetSpecificProfile(ListAPIView):
    permissions_classes = (IsAuthenticated, )
    serializer_class= AccountUpdateSerializer

    def get_queryset(self):

        pk=self.kwargs['id']
        return Insuree.objects.filter(user_id=pk)

class UpdateProfileDetails(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    
    lookup_field = 'user_id'
    queryset = Insuree.objects.all()
    serializer_class = AccountUpdateSerializer
