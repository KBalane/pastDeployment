from digiinsurance.models import Advertisement
from api.serializers import AdvertisementSerializer
from datetime import date
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

__all__ = ['AdvertisementUpdateStatus']

class AdvertisementUpdateStatus(APIView):
    def get(self, request):
        today = date.today()
        ads = Advertisement.objects.filter(Expiration_Date__lte=date(today.year, today.month, today.day)).update(Status='Inactive')
        return Response(status.HTTP_200_OK)