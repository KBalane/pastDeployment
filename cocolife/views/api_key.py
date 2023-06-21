from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from cocolife.serializers import APIKeySerailizer
from cocolife.models import APIKey

__all__ = ['APIKey', 'APIKeysByID']


class APIKeys(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerailizer


class APIKeysByID(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    lookup_field = 'id'
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerailizer
