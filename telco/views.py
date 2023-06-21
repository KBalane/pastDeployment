from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from digiinsurance.models import User, Insuree

from telco.models import TelcoPersonAddress, TelcoSimDetails, TelcoCompany, JumioToken
from telco.serializers import JumioTokenSerializer, TelcoCompanySerializer, TelcoPersonAddressSerializer, TelcoSimDetailsSerializer

from requests.auth import HTTPBasicAuth

import requests
import json

from datetime import datetime

class TokenVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        data = Token.objects.get(key = token)
        isValidToken = True if token == data.key else False
        
        res = {
            'isValidToken': isValidToken,
            'id': data.user.id,
            'token': data.key,
            'email': data.user.email
        }

        return Response(res)

# Address
class AddressViewLC(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = TelcoPersonAddress.objects.all()
    serializer_class = TelcoPersonAddressSerializer


class AddressViewRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'user'
    queryset = TelcoPersonAddress.objects.all()
    serializer_class = TelcoPersonAddressSerializer


# SIM Details
class SIMDetailsViewLC(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = TelcoSimDetails.objects.all()
    serializer_class = TelcoSimDetailsSerializer


class SIMDetailsViewRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = TelcoSimDetails.objects.all()
    serializer_class = TelcoSimDetailsSerializer

class SIMDetailsViewAllByID(APIView):
    permission_classes = (AllowAny,)
    queryset = TelcoSimDetails.objects.all()
    serializer_class = TelcoSimDetailsSerializer

    def get(self, request, user):
        queryset = self.queryset.filter(user = user)
        serializer_class = self.serializer_class(queryset, many=True)
        return Response(serializer_class.data)
    


# Company
class CompanyViewLC(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = TelcoCompany.objects.all()
    serializer_class = TelcoCompanySerializer


class CompanyViewRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = TelcoCompany.objects.all()
    serializer_class = TelcoCompanySerializer


class CompanyStoreFiles(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = TelcoCompany.objects.all()
    serializer_class = TelcoCompanySerializer

    def post(self, request):
        serializer = TelcoCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class CompanyRetrieveFiles(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TelcoCompanySerializer

    def get(self, request):
        today = datetime.now()
        start_date = request.data.get('start_date', '2021-01-01')
        end_date = request.data.get('end_date', today)

        query = TelcoCompany.objects.all().values(
            'cert_of_registration', 
            'resolution', 
            'power_attorney'
            ).filter(created_at__range=[start_date, end_date])

        context = {
            "files": query
        }
        return Response(context, status=status.HTTP_200_OK)


class CompanyFileByID(APIView):
    permission_classes = [AllowAny]
    serializer_class = TelcoCompanySerializer

    def get(self, request, id):
        try:
            context = {
                "Files": TelcoCompany.objects.filter(id=id).values(
                    'cert_of_registration',
                    'resolution',
                    'power_attorney',
                    )
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            return Response({
                "Error": "File doesn't Exist"
            }, status=status.HTTP_404_NOT_FOUND)


username = 'dlfmpd5oqij6bse9656lt4no9'
password = 'vl55jgbdnpb7vjjp68r9k5vsinijv63turm5hf81rp0jl9c331u'


class JumioGenerateToken(APIView):
    permission_classes = (AllowAny,)
    # serializer_class = GetPaymentDetailsSerializer

    def post(self, request):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # username = settings.CL_CORE_VL_KEY if serializer.data.get(
        #     'PolicyNumber')[0] == 'V' else settings.CL_CORE_TRAD_KEY
        payload = {
            "grant_type": "client_credentials"
        }
        headers = {
            'Authorization': 'Basic ZGxmbXBkNW9xaWo2YnNlOTY1Nmx0NG5vOTp2bDU1amdiZG5wYjd2ampwNjhyOWs1dnNpbmlqdjYzdHVybTVoZjgxcnAwamw5YzMzMXU=',
            'Cookie': 'XSRF-TOKEN=aad18344-7ab3-4c51-9fcd-43a8e8b7f86c',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        try:
            r = requests.post("https://auth.apac-1.jumio.ai/oauth2/token", auth=HTTPBasicAuth(
                'dlfmpd5oqij6bse9656lt4no9',
                'vl55jgbdnpb7vjjp68r9k5vsinijv63turm5hf81rp0jl9c331u'),
                headers=headers,
                data=payload)
            print(r)
        except Exception as e:
            return Response(str(e), status=400)

        if r.status_code == 200:  # access_token
            result = r.json()  # .get('access_token')
            return Response(result, status=200)
        else:
            return Response({"error": "jumio api error"}, status=400)


class JumioInitiateAccount(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_type = request.data['user_type']
        token = request.data['token']
        payload = {
            "customerInternalReference": user_type,
            "workflowDefinition": {
                "key": 10013,
                "credentials": [
                    {
                        "category": "ID",
                        "country": {
                            "predefinedType": "DEFINED",
                            "values": ["USA", "CAN", "AUT", "GBR"]
                        }
                    }
                ],
                "capabilities": {
                    "watchlistScreening": {
                        "additionalProperties": "string"
                    }
                }
            },
            "callbackUrl": "https://example.com",
            "userReference": "4"
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'User Demo',
            'Authorization': 'Bearer %s' % (token),
        }
        try:
            r = requests.post("https://account.apac-1.jumio.ai/api/v1/accounts", auth=None,
                headers=headers,
                data=json.dumps(payload))
            print(r)
        except Exception as e:
            return Response(str(e), status=400)

        if r.status_code == 200:  # access_token
            result = r.json()  # .get('access_token')
            return Response({
                "user_type": user_type, 
                "result": result
            }, status=200)
        else:
            return Response({"error": "jumio api error"}, status=400)

class JumioStatusAccount(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        token = self.request.query_params.get('token') #request.data['token']
        account_id = self.request.query_params.get('account_id') #request.data['account_id']
        workflow_id = self.request.query_params.get('workflow_id') #request.data['workflow_id']
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'User Demo',
            'Authorization': 'Bearer %s' % (token),
        }
        try:
            r = requests.get("https://retrieval.apac-1.jumio.ai/api/v1/accounts/%s/workflow-executions/%s/status" % (account_id,workflow_id), auth=None,
                headers=headers,
                data={})
            print(r)
        except Exception as e:
            return Response(str(e), status=400)

        if r.status_code == 200:  # access_token
            result = r.json()  # .get('access_token')
            return Response(result, status=200)
        else:
            return Response({"error": "jumio api error"}, status=400)

class JumioRetrieveAccount(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        token = self.request.query_params.get('token') #request.data['token']
        account_id = self.request.query_params.get('account_id') #request.data['account_id']
        workflow_id = self.request.query_params.get('workflow_id') #request.data['workflow_id']
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'User Demo',
            'Authorization': 'Bearer %s' % (token),
        }
        try:
            r = requests.get("https://retrieval.apac-1.jumio.ai/api/v1/accounts/%s/workflow-executions/%s" % (account_id,workflow_id), auth=None,
                headers=headers,
                data={})
            print(r)
        except Exception as e:
            return Response(str(e), status=400)

        if r.status_code == 200:  # access_token
            result = r.json()  # .get('access_token')
            return Response(result, status=200)
        else:
            return Response({"error": "jumio api error"}, status=400)

class JumioTokenLC(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = JumioToken.objects.all().order_by('-created_at')
    serializer_class = JumioTokenSerializer

class JumioTokenRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = JumioToken.objects.all()
    serializer_class = JumioTokenSerializer

class TelcoProfile(APIView):
    permission_classes = (AllowAny,)
    
    
    def get(self, request, user_id):

        res = {
            "user_details": User.objects.filter(id = user_id).values(),
            "user_details_extra": Insuree.objects.values('middle_name','gender').filter(user = user_id),
            "telco_address_details": TelcoPersonAddress.objects.filter(user = user_id).values(),
            "telco_sim_details": TelcoSimDetails.objects.filter(user = user_id).values(),
        }

        return Response(res)
    
    def put(self, request, user_id):

        user_details = User.objects.filter(id = user_id).update(
            username = request.data['username'],
			first_name = request.data['first_name'],
			last_name = request.data['last_name'],
			is_staff = request.data['is_staff'],
			is_active = request.data['is_active'],
			email = request.data['email'],
			info_submitted = request.data['info_submitted'],
			is_verified = request.data['is_verified'],
			country_code = request.data['country_code'],
			mobile_number = request.data['mobile_number'],
        )

        user_details_extra = Insuree.objects.filter(user = user_id).update(
            middle_name = request.data['middle_name'],
            gender = request.data['gender'],
        )

        telco_address_details = TelcoPersonAddress.objects.filter(user = user_id).update(
            province = request.data['province'],
        )
        
        telco_sim_details = TelcoSimDetails.objects.filter(user = user_id)
        if telco_sim_details.first() == None:
            TelcoSimDetails.objects.create(
            user = User.objects.get(id = user_id),
            name = request.data['sim_name'],
            number_owner = request.data['number_owner'],
            owner_relationship = request.data['owner_relationship'],
            minor_name = request.data['minor_name'],
            purpose = request.data['purpose'],
            sim_card_serial = request.data['sim_card_serial'],
            sim_card_number = request.data['sim_card_number'],
            isActive = request.data['isActive'],
            )
        else:
            telco_sim_details.filter(id = request.data['sim_id']).update(
            name = request.data['sim_name'],
            number_owner = request.data['number_owner'],
            owner_relationship = request.data['owner_relationship'],
            minor_name = request.data['minor_name'],
            purpose = request.data['purpose'],
            sim_card_serial = request.data['sim_card_serial'],
            sim_card_number = request.data['sim_card_number'],
            isActive = request.data['isActive'],
            )
        
        return Response(200)
