from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework import viewsets
from rest_framework.views import APIView


from django.core.files import File
from api.serializers import PolicyImageSerializer, GetAllPolicySerializer, GetPolicyBenefitsSerializer, PolicySerializer , DownloadPDFPolicySerializer
from digiinsurance.models import Policy
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response

import os
from django.conf import settings
from django.http import HttpResponse, Http404

__all__ = ['PolicyViewImage_Update','PolicyViewImage_POST']

class PolicyViewImage_Update(RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Policy.objects.all()
    serializer_class =  PolicyImageSerializer

    def PUT(self, request, id):
        try:
            Pol_obj = Policy.objects.get(id=id)
        except Policy.DoesNotExist:
            raise Http404

        serializer = PolicyImageSerializer(Pol_obj, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PolicyViewImage_POST(ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicyImageSerializer
