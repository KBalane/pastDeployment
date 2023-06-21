from digiinsurance.models import Advertisement
from api.serializers import AdvertisementSerializer, EditAdvertisementStatusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import  RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

__all__ = ['EditAdvertisement', 'EditAdvertisementStatus']


class EditAdvertisement(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

class EditAdvertisementStatus(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    queryset = Advertisement.objects.all()
    serializer_class = EditAdvertisementStatusSerializer

