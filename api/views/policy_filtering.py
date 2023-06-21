from api import serializers
from digiinsurance.models import Policy
from api.serializers import GetAllPolicySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin

__all__ = ['Policy_Filtering']

class Policy_Filtering(ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = GetAllPolicySerializer

    def get(self, request, status_search , *args, **kwargs):
        if status_search == 'all':
            self.queryset = Policy.objects.all()
        else: 
            self.queryset = Policy.objects.all().filter(status=status_search)
            
        return super().get(request, *args, **kwargs)




    # def get(self,request, status_search): # , current_user):

    #     #insuree_policy = InsureePolicy.objects.all().values('insuree__first_name').filter(status=status_search)
    #     if status_search == 'all':
    #         filter_policy = Policy.objects.all()
    #     else: 
    #         filter_policy = Policy.objects.all().filter(status=status_search) # , insuree=current_user)
    #     seriallzer = GetAllPolicySerializer(filter_policy,many=True)
    #     return Response((seriallzer.data))

    
    
