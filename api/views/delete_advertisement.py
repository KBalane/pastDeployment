from digiinsurance.models import Advertisement
from api.serializers import AdvertisementSerializer, EditAdvertisementStatusSerializer, DeleteAdvertisementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import  RetrieveUpdateAPIView, UpdateAPIView, RetrieveDestroyAPIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

__all__ = ['DeleteAdvertisement']


class DeleteAdvertisement(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    queryset = Advertisement.objects.all()
    serializer_class = DeleteAdvertisementSerializer

    def get(self, request, id):
        query = Advertisement.objects.all().values().filter(id=id)
        return Response(query[0])

    def delete(self, request, id, **kwargs):
        try:
            ifexists = Advertisement.objects.filter(id=id)
            ifexists.delete()
            return Response({'message': 'Advertisement was deleted successfully!'})
        except Exception:
            pass
        return super().delete(request, **kwargs)
