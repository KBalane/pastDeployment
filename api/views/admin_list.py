from digiinsurance.models import User, Insuree
from api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

__all__ = ['Admin_List']

class Admin_List(APIView):
    def get(self, request):
        #check sticky "role": "AD"
        admins = Insuree.objects.all().values(
            'user',
            'last_name',
            'first_name',
            'middle_name',
            'user__username',
            'mobile_number',
            'email',
            'user__role',
            ).filter(user__role='AD')
        return Response(admins)
        

