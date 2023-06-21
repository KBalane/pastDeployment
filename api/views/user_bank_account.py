from rest_framework import viewsets
# from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from api.serializers import UserBankAccountSerializer
from digiinsurance.models import UserBankAccount

__all__ = ['UserBankAccountViewSet','BankAccountsGetSpecific','UpdateBankAccount']


class UserBankAccountViewSet(viewsets.ModelViewSet):
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserBankAccount.objects.all()
        user = self.request.query_params.get('user')
        new_bank_accounts = []
        if user:
            queryset = queryset.filter(user=user)

        for bank_account in queryset:
            # bank_account.account_number = bank_account.account_number[:6] + 'X' * 6 + bank_account.account_number[-4:]
            # bank_account.account_number = bank_account.account_number[-4:].rjust(len(bank_account.account_number), "X")
            # masking will be done in the front end since both masked and unmasked values are needed
            new_bank_accounts.append(bank_account)

        return new_bank_accounts
        
class UpdateBankAccount(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBankAccountSerializer
     
class BankAccountsGetSpecific(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )

    queryset = UserBankAccount.objects.all()
    serializer_class = UserBankAccountSerializer