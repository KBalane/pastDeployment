from digiinsurance.models import User, Insuree
from api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated


__all__ = ['Admin_Edit','AdminUpdate']

class AdminUpdate(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, id):
        #lookup_field ='id'
        queryset = Insuree.objects.all().values(
            'user_id',
            'user__username',
            'email',
            'mobile_number',
            'first_name',
            'middle_name',
            'last_name',
            'user__role',
        ).filter(user_id=id)
        return Response(queryset)
    
    def put(self, request, id):
        #id = request.query_params["id"]
        '''
        username = User.objects.values(
            'username'
            ).filter(id=id).update(
                username = request.data.get("username"),
                role = request.data.get("role"),
            )
        '''

        users = Insuree.objects.all().values(
            'user_id',
            'user__username',
            'user__role',
            'email',
            'mobile_number',
            'first_name',
            'middle_name',
            'last_name',
        ).filter(user_id=id).update(
            email= request.data.get("email"),
            mobile_number= request.data.get("mobile_number"),
            first_name = request.data.get("first_name"),
            middle_name = request.data.get("middle_name"),
            last_name = request.data.get("last_name"),
            )

        User.objects.filter(id=id).update(
                username = request.data.get("user__username"),
                role = request.data.get("user__role"),
                )

        updated_data = Insuree.objects.all().values(
            'user_id',
            'user__username',
            'email',
            'mobile_number',
            'first_name',
            'middle_name',
            'last_name',
            'user__role',
        ).filter(user_id=id)

        return Response(updated_data)

"""
class AdminUpdate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )

    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""

class Admin_Edit(APIView):
    #(self, request, *args, **kwargs):
    def put(request,pk):
        users = User.objects.get(id=pk)
        serializer = UserSerializer(users, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["sucesss"] = "Update Successful"
            return Response(data = data)
        return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)




'''
admin_create:
{
        "id": 460,
        "username": "vankeith",
        "email": "vkalmazan@gmail.com",
        "role": "AD",
        "photo": "/media/users/460.PNG",
        "country_code": "+69",
        "mobile_number": "09055645643",
        "kyc_done": false,
        "info_submitted": false
    },

admin_update: (insuree model)
{
        "user_id": 460,
        "user__username": "vankeith",
        "user__role": "AD",
        "user__photo": "/media/users/460.PNG",
        "user__country_code": "+69",
        "user__mobile_number": "09055645643",
        "user__kyc_done": false,
        "user__info_submitted": false,
        "email": "hotbabes@gmail.com",
        "mobile_number": "09174563245",
        "first_name": "Van Keith",
        "middle_name": "Smith",
        "last_name": "Almazan",
        
    }
'''
        
