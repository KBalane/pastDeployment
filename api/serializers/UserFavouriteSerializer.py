from rest_framework import serializers
from digiinsurance.models.UserFavourite import Favourites
from rest_framework import serializers, exceptions

__all__ = ['UserFavouriteSerializer']


class UserFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'
