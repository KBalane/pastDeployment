from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import CompanyFAQSerializer
from digiinsurance.models import CompanyFAQ
__all__ = ['CompanyFAQCreate', 'CompanyFAQUpdate']

class CompanyFAQCreate(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = CompanyFAQ.objects.all()
    serializer_class = CompanyFAQSerializer
       
class CompanyFAQUpdate(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = CompanyFAQ.objects.all()
    serializer_class = CompanyFAQSerializer



        
        
    