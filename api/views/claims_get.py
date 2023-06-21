from digiinsurance.models import Claims, InsureePolicy
from api.serializers import ClaimsSerializer

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.generics import GenericAPIView
from django.shortcuts import render

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


@api_view(['GET'])
def claims_get(request):
    
    if request.method == 'GET':
        claims = Claims.objects.all()
        tutorials_serializer = ClaimsSerializer(claims, many=True)
        return Response(tutorials_serializer.data)
        # 'safe=False' for objects serialization
    
