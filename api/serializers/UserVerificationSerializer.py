from rest_framework import serializers

from kyc.models import UserID
from digiinsurance.models.User import User

__all__ = ['GetUserVerificationSerializer', 'GetUserKYCVerificationSerializer']


class GetUserVerificationSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('is_verified', )


class GetUserKYCVerificationSerializer(serializers.Serializer):
    class Meta:
        model = UserID
        fields = ('verified',)

