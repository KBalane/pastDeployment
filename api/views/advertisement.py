import logging
from digiinsurance.models import Advertisement
from api.serializers import AdvertisementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import  RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
import re 
__all__ = ['Advertisement']

logger = logging.getLogger('api.views')
class Advertisement(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def post(self, request, *args, **kwargs):
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["Link"] = re.sub('https://','',serializer.validated_data["Link"])
            serializer.save()
        
        try:
            id = serializer.data['id']
            date_today = serializer.data['Publish_Date']
            date_expired = serializer.data['Expiration_Date']
            new_object = self.queryset.values(
                'Publish_Date',
                'Expiration_Date').filter(id=id)
            if date_today > date_expired:
                new_object.update(Status = 'Inactive')
            else:
                new_object.update(Status = 'Active')
            
            new_object = self.queryset.filter(id=id)
            serializer = self.serializer_class(new_object, many=True)
        except Exception as e:
            logger.exception(e)
            return Response({
                'status': "Not a valid product"
            })
        
        return Response(serializer.data)