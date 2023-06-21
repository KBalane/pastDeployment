from digiinsurance.models import User
from digiinsurance.models import InsureePolicy

from api.serializers import UserSerializer as apiuser
from api.serializers import InsureePolicySerializer

from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import JsonResponse

from rest_framework import serializers

__all__ = ['Active_Policy_User']

class Active_Policy_User(APIView):
    def get(self,request):
        active_policy_users = InsureePolicy.objects.all().filter(status="active").count()
        active_users = User.objects.all().filter(is_active=True).count()
        #user_bank_account = UserBankAccount.objects.all().values_list("account_number","created_at","account_name")
        #serializer = InsureePolicySerializer(active_policy_users,many=False)
        context = { 
            "active_policy_users": active_policy_users,
            "active_users": active_users}
        return Response(context)