from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserBankAccountSerializer
from digiinsurance.models import UserBankAccount
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from api.utils import get_twilio_client
from rest_framework.response import Response

__all__ = ['GetSpecificBankAccount', 'PhoneVerification','PhoneVerification_check']

@api_view(['GET', 'PUT', 'DELETE'])
def GetSpecificBankAccount(request, pk):

    bank_account_serializer = UserBankAccountSerializer
    permission_classes = [IsAuthenticated]
    try: 
        bank_account = UserBankAccount.objects.get(pk=pk) 
    except UserBankAccount.DoesNotExist: 
        return JsonResponse({'message': 'The account does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        bank_account_serializer = UserBankAccountSerializer(bank_account)
        return JsonResponse(bank_account_serializer.data) 

    elif request.method == 'PUT': 
        bank_account_data = JSONParser().parse(request) 
        bank_account_serializer = UserBankAccountSerializer(bank_account, data=bank_account_data) 
        if bank_account_serializer.is_valid(): 
            bank_account_serializer.save() 
            return JsonResponse(bank_account_serializer.data) 
        return JsonResponse(bank_account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': 
        bank_account.delete() 
        return JsonResponse({'message': 'Account was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class PhoneVerification(APIView):
    def post(self, request):
        user_phone_number = request.data.get('mobile_number')
        verify_phone = get_twilio_client()

        verify_phone.verifications.create(to = user_phone_number, channel='sms')

        message = "Verification Sent!!"

        return Response(message)

class PhoneVerification_check(APIView):
    def post(self, request, mobile_number):
        code = request.data.get('code')
        verify_phone = get_twilio_client()

        verification_status = verify_phone.verification_checks.create(to = mobile_number, code=code)
        
        if verification_status.status == 'approved':
            success_message = "Your mobile number has been verified."

            return Response(success_message) 
        else:
            error_message = "Wrong code!!"

            return Response(error_message)