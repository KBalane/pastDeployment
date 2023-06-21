from rest_framework import serializers

from digiinsurance.models import Claims
from api.utils import generate_claims_refno
__all__ = ['ClaimsSerializer','ClaimsDocsSerializer']


class ClaimsSerializer(serializers.ModelSerializer):
    # TO BE INCLUDED ONCE CLAIMS_REFNO IS REQUIRED BY THE COMPANY 
    # ALSO CHECK generate_claims_refno FOR MODIYING REF_NO. GENERATOR
    # claims_refno = serializers.CharField(default=id)
    class Meta:
        model = Claims
        fields = ('claim_docs','UserPolicy_id', 'claim_type', 'bank_name','id','claims_refno', 'claim_status')


class ClaimsDocsSerializer(serializers.ModelSerializer):
    # TO BE INCLUDED ONCE CLAIMS_REFNO IS REQUIRED BY THE COMPANY 
    # ALSO CHECK generate_claims_refno FOR MODIYING REF_NO. GENERATOR
    # claims_refno = serializers.CharField(default=id)
    class Meta:
        model = Claims
        fields = ('id', 'claims_refno', 'modified_at', 'UserPolicy_id', 'claim_type', 'claim_docs', 'bank_name',
                  'claim_status')

