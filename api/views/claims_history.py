from digiinsurance.models import Claims, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView

__all__ = ['Claims_History','ClaimsHistoryPerUser']

class Claims_History(APIView):
    def get(self,request, policyid_filter): 

        claims_transaction_history = Transaction.objects.all().values(
            'id',
            'insureePolicy__policy',
            'txn_id',
            'transaction_date',
            'description'
        ).order_by('-transaction_date').filter(insureePolicy__policy = policyid_filter)



        """
        Choices are: amount, archived, archived_at, channel, company, 
        company_id, completed_at, created_at, fee, id, insuree, 
        insureePolicy, insureePolicy_id, insuree_id, modified_at, 
        payment_type, processor, processor_type, transaction_date, 
        txn_id, updated_at, vat
        """
        
        context = {
            "claims_history" : claims_transaction_history
        }
                

        return Response(context)


class ClaimsHistoryPerUser(APIView):
    """
    Retrieves the Claims History Per User
    """
    def get(self,request, user_id): 
        claims_per_user = Claims.objects.all().values(
            'id',
            'UserPolicy_id__insuree', #'insuree_id',
            'UserPolicy_id', #'insureePolicy__policy',
            'claims_refno', #'txn_id',
            'modified_at', #'transaction_date',
            #'details', #'description'
        ).order_by('-modified_at').filter(UserPolicy_id__insuree = user_id)
        context = {
            "claims_history_per_user" : claims_per_user
        }
        return Response(context)

        """
        Choices are: UserPolicy_id, UserPolicy_id_id, 
        amount, bank_name, claim_docs, claim_type, 
        claims_refno, details, document, id, modified_at
        """


