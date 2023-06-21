from cocolife.models import CLAdvertisements
from datetime import date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

__all__ = ['UpdateAdvertisementStatus']


class UpdateAdvertisementStatus(APIView):
    def get(self, request):
        today = date.today()
        ads = CLAdvertisements.objects.filter(expiration_date__lte=date(
            today.year, today.month, today.day)).update(status='Inactive')
        return Response(status.HTTP_200_OK)
