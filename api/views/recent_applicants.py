from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView

from digiinsurance.models.UserBankAccount import UserBankAccount
from digiinsurance.models.User import User
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.Insuree import Insuree

from api.serializers.UserBankAccountSerializer import UserBankAccountSerializer
from api.serializers.AccountSerializer import AccountInfoSerializer

from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

__all__ = ['Recent_Application', 'recent_application_not_final', 'recent_application', 'getTest3', 'UserField']


class Recent_Application(APIView):
    def get(self, request):
        users = Insuree.objects.order_by('-created_at')[:5]
        insuree_users = InsureePolicy.objects.values(
            'insuree__user_id',
            'created_at',
            'status'
        ).annotate(name=Concat(
            'insuree__first_name', V(' '),
            'insuree__last_name', V(''),
            output_field=CharField())).order_by('-created_at')

        serializer = AccountInfoSerializer(users, many=True)
        context = {"top_5_new_applications": insuree_users}
        return Response(context)


class UserField(APIView):
    def get(self, request):
        path = str.split(str(request.path), '/')
        print(path)
        fieldname = path[4]  # check your path on the print
        if fieldname == 'account_name':
            content = {'account_name': User.objects.get(pk=path[6]).username}
            content = {'account_name': 'account_name'}
            return Response(content)


class getTest3(CreateAPIView):
    user_bank_account = UserBankAccount.objects.all()[:5]
    user_bank_account = user_bank_account.values('account_number', 'created_at', 'account_name')
    # serializer_class = insureePolicies.objects.all()


@api_view(['GET'])
def recent_application_not_final(request):
    if request.method == 'GET':
        user_bank_account = UserBankAccount.objects.all().values_list(
            'user__user__Insuree__status', "account_number", "created_at", "account_name")
        # still need status
        return Response(user_bank_account)

        # user_bank_account = user_bank_account.values('account_number','created_at','account_name','user')
        # user_bank_account = UserBankAccount.objects.filter(user__insuree=44)
        # queryset = UserBankAccount.objects.raw('SELECT UserBankAccount.account_number, UserBankAccount.created_at,
        # users.name from UserBankAccount inner join users on UserBankAccount.user = users.user')
        # serializer_class = UserBankAccountSerializer
        # return Response(serializer_class.data)
        # query_set = UserBankAccount.objects.raw(r'select * from UserBankAccount')
        # ModelName.objects.values('Colum_name')
        # ManagedModel.objects.all().defer('f2')
        # user_bank_account = UserBankAccount.objects.raw('Select * from digiinsurance_userbankaccount')
        # users = user.get_queryset()


@api_view(['GET'])
class recent_application(viewsets.ModelViewSet):
    def recent_application(request):
        if request.method == 'GET':
            queryset = UserBankAccount.objects.raw(' '
                                                   + 'SELECT account_number, created_at, '
                                                   + 'account_name, status '
                                                   + 'FROM digiinsurance_UserBankAccount '
                                                   + 'INNER JOIN digiinsurance_insureepolicy '
                                                   + 'ON userbankaccount_account_name = insureepolicy_insuree ')
            serializer_class = UserBankAccountSerializer

        """
        status_on_user = InsureePolicy.objects.values(
            'insuree_id','created_at','policy__name','status'
            ).filter(insuree=current_user) 
        

        user_bank_account = UserBankAccount.objects.values(
            "account_number","created_at","account_name",'user', 'user_id','user__is_verified'
            ).filter(user_id=current_user)
        
        context = {
            "bank_details" : user_bank_account,
            "status" : status_on_user
        }
        
        """
