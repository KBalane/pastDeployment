import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from digiinsurance.models import User
from kyc.models import UserID

from api.serializers import GetUserVerificationSerializer, GetUserKYCVerificationSerializer


__all__ = ['GetUserVerification', 'GetUserKYCVerification']

class GetUserVerification(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class =  GetUserVerificationSerializer

    def get(self, request, user_id):
        user_verification = User.objects.filter(id = user_id).values('is_verified')

        context = {
            'status':user_verification
        }

        return Response(context)

class GetUserKYCVerification(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = GetUserKYCVerificationSerializer

    def get(self, request, user_id):
        userkyc_verification = UserID.objects.filter(user_id= user_id).values('verified')

        context = {
            'status':userkyc_verification
        }

        return Response(context)