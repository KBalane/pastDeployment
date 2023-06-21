from digiinsurance.models import Claims
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.db.models import Sum


__all__ = ['Claims_Details']


class Claims_Details(APIView):
    def get(self,request, id_search): 
        name = Claims.objects.all().values('id').annotate(policy_holder=Concat(
                'UserPolicy_id__insuree__first_name',
                V(' '), 'UserPolicy_id__insuree__last_name', V(''),
                output_field=CharField()
                )).filter(id = id_search)

        user_account_number = Claims.objects.all().values(
            'UserPolicy_id__insuree__user_id'
            ).filter(id = id_search)

        claim_number = Claims.objects.all().values(
            'id'
        ).filter(id = id_search)

        policy_type_id = Claims.objects.all().values(
            'UserPolicy_id__policy_type',
            'UserPolicy_id__policy'
        ).filter(id = id_search)

        claim_completed_date = Claims.objects.all().values(
            'modified_at'
        ).filter(id = id_search)

        total_payments = Claims.objects.all().values(
            'amount'
        ).filter(id = id_search).aggregate(total = Sum('amount'))

        claim_status = Claims.objects.all().values(
            'UserPolicy_id__status'
        ).filter(id = id_search)


        """ risk_details = Claims.objects.all().values(
            'details'
        ).filter(id = id_search) """


        
        gender = Claims.objects.all().values(
            'UserPolicy_id__insuree__gender'
        ).filter(id = id_search)

        claim_created_on = Claims.objects.all().values(
            'modified_at'#'created_at'
        ).filter(id = id_search)

        claim_status_2 = Claims.objects.all().values(
            'claim_status'
        ).filter(id = id_search)

        context = {
            "name": name,
            "user_account_num" : user_account_number,
            "claim_number" : claim_number,
            "policy_type_id" : policy_type_id,
            "claim_completed_date" : claim_completed_date,
            "claim_created_date" : claim_created_on,
            "total_payments" : total_payments,
            "claim_status" : claim_status,
            #"risk_details" : risk_details,
            "gender": gender,
            "claim_status_2": claim_status_2
        }
                
        return Response(context)