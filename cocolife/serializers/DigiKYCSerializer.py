from rest_framework import serializers

from cocolife.models.DigiKYC import DigiUserID
from kyc.models import TemplateID

__all__ = ['DigiTemplateIDSerializer', 'DigiUpdatePhoto_idSerializer',
           'DigiUpdateSelfieSerializer', 'DigiUpdateKYC']


class DigiTemplateIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateID
        fields = ('id', 'template_name')


class DigiUpdatePhoto_idSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField()
    photo_id = serializers.CharField()
    photo_id_back = serializers.CharField()

    class Meta:
        model = DigiUserID
        fields = ('template_id', 'photo_id', 'photo_id_back')


class DigiUpdateSelfieSerializer(serializers.ModelSerializer):
    selfie = serializers.CharField()

    class Meta:
        model = DigiUserID
        fields = ('selfie', )


class DigiUpdateKYC(serializers.ModelSerializer):
    template_id = serializers.IntegerField()
    photo_id = serializers.CharField()
    photo_id_back = serializers.CharField()
    selfie = serializers.CharField()

    class Meta:
        model = DigiUserID
        fields = ('template_id', 'photo_id', 'photo_id_back', 'selfie', )
