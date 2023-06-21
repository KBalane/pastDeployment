# path('admin/claims/approve/<int:claim_id>/',views.ApproveUser.as_view(), name='Approve Claim'),
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime



from digiinsurance.models import Claims, User


__all__ = [  'ApproveClaims','DeniedClaims', ]



class ApproveClaims(APIView): 
    def get(self, request, claim_id):
        now = datetime.now()
        approve= Claims.objects.filter(id = claim_id).update(claim_status='approved')
        return Response(str(claim_id) + " is Approved.")

class DeniedClaims(APIView):
    def get(self, request, claim_id):
        approve = Claims.objects.filter(id = claim_id).update(claim_status='denied')
        return Response(str(claim_id) + " is Denied.")







