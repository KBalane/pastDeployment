import re
from cocolife.models import CLAdvertisements
from cocolife.serializers.AdvertisementSerializer import DigiAdvertisementSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

__all__ = ['PostAdvertisement']


class PostAdvertisement(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = CLAdvertisements.objects.all()
    serializer_class = DigiAdvertisementSerializer

    def post(self, request, *args, **kwargs):

        serializer = DigiAdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["link"] = re.sub(
                'https://', '', serializer.validated_data["link"])
            serializer.save()

        try:
            id = serializer.data['id']
            date_today = serializer.data['publish_date']
            date_expired = serializer.data['expiration_date']
            new_object = self.queryset.values(
                'publish_date',
                'expiration_date').filter(id=id)
            if date_today > date_expired:
                new_object.update(status='Inactive')
            else:
                new_object.update(status='Active')

            new_object = self.queryset.filter(id=id)
            serializer = self.serializer_class(new_object, many=True)
        except Exception as e:
            return Response({
                'status': "Not a valid product"
            })

        return Response(serializer.data)
