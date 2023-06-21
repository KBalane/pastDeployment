from rest_framework import serializers
from cocolife.models import CLAdvertisements

__all__ = ['DigiAdvertisementSerializer',
           'EditDigiAdvertisementStatusSerializer', 'DeleteDigiAdvertisementSerializer']


class DigiAdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = CLAdvertisements
        fields = ('__all__')


class EditDigiAdvertisementStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CLAdvertisements
        fields = ('status',)


class DeleteDigiAdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = CLAdvertisements
        fields = ('__all__')
