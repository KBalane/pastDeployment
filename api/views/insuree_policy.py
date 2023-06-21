from rest_framework import viewsets

from api.serializers.InsureeSerializer import InsureePolicySerializer, InsureePolicySerializer2
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.Beneficiaries import Beneficiaries
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response as R2

__all__ = ['InsureePolicyViewSet', 'InsureePolicyViewSet2']


class InsureePolicyViewSet(viewsets.ModelViewSet):
    queryset = InsureePolicy.objects.all()
    serializer_class = InsureePolicySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = InsureePolicy.objects.all().order_by('-insuree')
        insuree = self.request.query_params.get('insuree')
        if insuree:
            queryset = queryset.filter(insuree_id=insuree)
        return queryset


class InsureePolicyViewSet2(APIView):
    """
    Beneficary ID is below under 'beneficary'.
    This displays the beneficary_id for the corresponding insureepolicy/user_policy.
    """
    # queryset = InsureePolicy.objects.all()
    # serializer_class = InsureePolicySerializer2
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        cursor = connection.cursor()    
        cursor.execute("""select *,digiinsurance_beneficiaries.id as 'beneficary_id' from digiinsurance_insureepolicy
        inner join digiinsurance_beneficiaries 
        on digiinsurance_insureepolicy.id = digiinsurance_beneficiaries.user_policy_id""")
        row = cursor.fetchall()
        return R2(row)
        '''
        id_ = InsureePolicy.objects.all().values_list('id')
        queryset = InsureePolicy.objects.all().values(
            'id',
            'created_at',
            'modified_at',
            'status',
            'premium_amount_due',
            'premium_date_due',
            'premium_last_paid',
            'premium_last_date',
            'policy_type',
            'active_premium_interval',
            'policy',
            'insuree',
            'Currency',
            'policy_type2',
        )  # .filter(id__in=Beneficiaries.objects.all().values('id'))
        beneficiaries = Beneficiaries.objects.all().values('user_policy_id', 'id')
        context = {
            # "id": id_,
            'insureepolicy': queryset,
            'beneficiaries': beneficiaries
        }
        return R2(context)
