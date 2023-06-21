from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime



from api.serializers import GetInsureeTransactionSerializer, UserSerializer
from digiinsurance.models import Transaction, Insuree, User


__all__ = [ 'GetInsureeTransactionsView', 'ArchiveUser','UnArchiveUser','ListOfArchivedUsers']


class GetInsureeTransactionsView(ListAPIView):
    serializer_class = GetInsureeTransactionSerializer
    paginate_by = 10

    def get_queryset(self):
        insuree = self.kwargs['insuree']
        return Transaction.objects.filter(insuree=insuree)

class ArchiveUser(APIView): #also made one for policy holder in policy_holders.py
    def get(self, request, insuree_id):
        now = datetime.now()
        archive = Insuree.objects.filter(user__id = insuree_id).update(isArchived=True,modified_at=now)
        return Response(str(insuree_id) + " is now Archived.")

class UnArchiveUser(APIView):
    def get(self, request, insuree_id):
        archive = Insuree.objects.filter(user__id = insuree_id).update(isArchived=False)
        return Response(str(insuree_id) + " is an Active User again.")

class ListOfArchivedUsers(APIView):
    def get(self, Request):
        archivedUsers = Insuree.objects.all().values(
            'user',
            'user__username',
            'user__email',
            'user__photo',
            'user__country_code',
            'user__mobile_number',
            'user__info_submitted',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'created_at',
            'isArchived',
        ).filter(isArchived = True).order_by('-modified_at')
        
        return Response(archivedUsers)
