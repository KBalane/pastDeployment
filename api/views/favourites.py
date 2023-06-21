from digiinsurance.models import Favourites
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView
from django.http import HttpResponse, Http404
from api.serializers import UserFavouriteSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

__all__ = ['UserFavorite', 'UpdateFavourite']

class UserFavorite(ListCreateAPIView):
    queryset = Favourites.objects.all()
    serializer_class = UserFavouriteSerializer

class UpdateFavourite(RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Favourites.objects.all()
    serializer_class = UserFavouriteSerializer
