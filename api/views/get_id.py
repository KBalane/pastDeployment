from kyc.models import TemplateID, UserID
from api.serializers import  GetsubmittedID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView

__all__ = ['User_ID']

class User_ID(generics.ListAPIView):
    serializer_class = GetsubmittedID

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserID.objects.filter(user=user_id)
        

