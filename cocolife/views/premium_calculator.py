
from api import serializers
from digiinsurance.models import Policy
from api.serializers import GetAllPolicySerializer

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers import GetAllPolicySerializer
from rest_framework.views import APIView
from cocolife.serializers import PackagesJSONSerializer


import json

__all__ = ['IPAPremiumCalculator']

class IPAPremiumCalculator(APIView):
    # TODO - Make Authenticated
    permission_classes = (AllowAny,)
    def get(self,request):
        queryset = Policy.objects.all().filter(id = 1)
        serializer_class = GetAllPolicySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get(self,request):
        age = request.data.get('age')
        coverage_term = request.data.get('coverage_term')
        payment_term = request.data.get('payment_term')
        id = 1

        
        queryset = Policy.objects.all().filter(id = id)
        #face_amount = Policy.objects.all().values('packages').get(jsonfield__contains={'name':'Protect'})#.get(jsonfield__contains={'face_amount'})
        packages = Policy.objects.all().filter(id=id)
        packagesSerializer = PackagesJSONSerializer(packages, many=True)
        
        data_x = packagesSerializer.data
        benefits = []
        for x in packagesSerializer.data[0]['packages']:
            benefits.append(x['name'])
            benefits.append(x['benefits'])
        return Response(benefits)



        # cursor = connection.cursor()
        # cursor.execute("""
        #     SELECT JSON_EXTRACT(packages, '$[0].benefits') 
        #     as benefits 
        #     FROM digiinsurance.digiinsurance_policy where id = %s;
        #     ;""", [id])

        # benefits = cursor.fetchall()
        # return Response(benefits)
    