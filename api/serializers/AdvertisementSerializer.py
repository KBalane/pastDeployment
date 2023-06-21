from digiinsurance.models.Advertisement import Advertisement
from rest_framework import serializers


__all__ = ['AdvertisementSerializer', 'EditAdvertisementStatusSerializer', 'DeleteAdvertisementSerializer']


class AdvertisementSerializer(serializers.ModelSerializer):
    """
    def create(self,validated_data):

        if date.today() > validated_data['Expiration_Date']:
            validated_data['Status'] = 'Inactive'
        else:
            validated_data['Status'] = 'Active'

        #return Advertisement.objects.create(**validated_data)
        #instance = Advertisement.objects.create(**validated_data)
        #users = User.objects.filter(id__in = instance.policy)
        #instance.liked.set(users)

    #liked = serializers.IntegerField(required=False)
    """

    class Meta:
        model = Advertisement
        fields = '__all__'


class EditAdvertisementStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('Status',)


class DeleteAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
