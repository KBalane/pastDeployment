from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from django.core.files import File
from api.serializers import CreateProductSerializer
from digiinsurance.models import Policy

#__all__ = ['CreateProduct']


#class CreateProduct(CreateAPIView):
@api_view(['POST'])
def add_product(request):

   
    
    if request.method == 'POST':
        tutorial1_data = request.data #JSONParser().parse(request)
        
        tutorial1_serializer = CreateProductSerializer(data=tutorial_data)
        if tutorial1_serializer.is_valid():
            tutorial1_serializer.save()
            return Response(tutorial1_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(tutorial1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)