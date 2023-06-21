from rest_framework import serializers

from kyc.models import TemplateID, UserID


__all__ = ['TemplateIDSerializer', 'KYCListSerializer', 'PostIdandSelfieKycSerializer','AvatarSelfieSerializer','UpdatePhoto_idSerializer','UpdateSelfieSerializer', 'GetsubmittedID']


class TemplateIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateID
        fields = ('id', 'template_name')


class KYCListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserID
        fields = ('id', 'photo_id', 'selfie', 'user', 'template')


class PostIdandSelfieKycSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField()
    id_image = serializers.CharField()
    id_back_image = serializers.CharField()
    selfie_image = serializers.CharField()

    class Meta:
        model = UserID
        fields = ('template_id', 'id_image', 'id_back_image', 'selfie_image')


class UpdatePhoto_idSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField()
    id_image_front = serializers.CharField()
    id_image_back = serializers.CharField()

    class Meta:
        model = UserID
        fields = ('template_id','id_image_front','id_image_back')


class UpdateSelfieSerializer(serializers.ModelSerializer):
    selfie_image = serializers.CharField()

    class Meta:
        model= UserID
        fields = ('selfie_image', )


class AvatarSelfieSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserID
        fields = ('id', 'selfie')


class GetsubmittedID(serializers.ModelSerializer):
    class Meta:
        model = UserID
        fields = ('id', 'photo_id', 'photo_id_back', 'user', 'template')