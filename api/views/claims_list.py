from api.utils import generate_claims_refno
from api.serializers import ClaimsSerializer
from api.tasks import send_claims_confirmation

from digiinsurance.models import Claims, User
from digiinsurance import settings
from digiinsurance.storage_backend import get_s3_client

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.tasks import send_verification_email
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V, F

__all__ = ['Claims_List', 'UploadClaims']

class Claims_List(APIView):
    def get(self,request): 
        list_of_claims = Claims.objects.all().values(
            'id',
            'UserPolicy_id',
            'modified_at',
            'UserPolicy_id__status',
            'claim_type', #still needs claim type column that is not present in claim model
            'UserPolicy_id__policy_type',
            'UserPolicy_id__policy_type2',
            'claim_status',
            ).annotate(policy_holder=Concat(
                'UserPolicy_id__insuree__first_name',
                V(' '), 'UserPolicy_id__insuree__last_name', V(''),
                output_field=CharField()
                )).annotate(user_id=F(
                'UserPolicy_id__insuree__user_id',
                )).order_by('-modified_at')
        context = {
            "claims_list" : list_of_claims
        }
                
        return Response(context)

class UploadClaims(APIView):
    def get_upload_claims_cloud(self, context, request):
        if settings.IS_PRODUCTION:
            serializeddata = context

            # User_policy_id = request.data.get('UserPolicy_id')
            claims_id = serializeddata.get('id')
            claims_doc = Claims.objects.get(id=claims_id)
            file = open(claims_doc.claim_docs.path, 'rb')
            file_key = 'claims_documents/claims_%s' % (claims_id)
            client = get_s3_client()
            client.put_object(Bucket = settings.AWS_STORAGE_BUCKET_NAME, Key = file_key, Body=file, ACL='private')

            success_message = "Successfully upload."

            return success_message

    def post(self, request, user_id):
        # user_id = request.user
        user = User.objects.get(id = user_id)

        serializer = ClaimsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            Policy_id = serializer.data.get('UserPolicy_id')
            Claims_id = serializer.data.get('id')
            #claims_refno = generate_claims_refno()
            claims = Claims.objects.filter(id=Claims_id).update(
                claims_refno = generate_claims_refno()
            )

            context ={
                'Policy_id':Policy_id,
                'Claims_id':Claims_id,
            }

            #send_claims_confirmation.delay(user.id, context)
            send_claims_confirmation(user.id, context)
            
            if settings.IS_PRODUCTION:
                context = serializer.data
                return Response(self.get_upload_claims_cloud(context, request))
            return Response(context,  status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)