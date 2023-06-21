import logging

from decimal import Decimal

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, ListAPIView

from datetime import datetime

from digiinsurance.models import CompanyInvestmentType, UserInvestment, User, InsureePolicy, Insuree
from digiinsurance.models import Investment

# from api.tasks import send_investment_confirmation
from api.serializers import CompanyInvestmentTypeSerializer, UserInvestmentSerializer, UserInvestmentUploadSerializer, GetUserInvestmentSerializer
from api.utils import generate_transaction_id
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

logger = logging.getLogger('digiinsurance.views')

__all__ = ['UserInvestmentCalculator', 'UserInvestmentUpload','GetCompanyInvestmentType','GetUserInvestmentStatus','GetListOfUserInvestment','UploadInvestmentProduct']

class UserInvestmentCalculator(CreateAPIView):
    permissions_classes=(IsAuthenticated, )
    serializer_class = UserInvestmentSerializer

    def post(self, request):
        # user = User.objects.get(id = user_id)
        investment_type = CompanyInvestmentType.objects.filter(company = request.data.get('company_id'))
        initial_dep = request.data.get('initial_dep')
        succeeding_dep = request.data.get('succ_dep_amount')
        end_year = request.data.get('end_year_payment')


        current_year = datetime.today().year
        print(current_year)
        total_year = end_year - current_year

        total_investment = initial_dep + (succeeding_dep * total_year)
        print(total_investment)

        fund_type = []
        risked_investments = []

        for investment_risk in investment_type:
            fund_type.append(investment_risk.investment_name)
            print(investment_risk.investment_name)
            rounded_value = round(total_investment * (1 + (investment_risk.risk_rate * total_year)), 2)
            risked_investments.append(rounded_value)
        
        # computation for time deposit  
        time_deposit = total_investment + ((total_investment * 0.0025)*((365 * total_year)/ 365)* .8)

        #computation for savings
        savings_interest = total_investment + (total_investment * 0.02 * 1)

        context = {
            'total_investment':total_investment,
            'years_of_payment':total_year,
            'fund_type':fund_type,
            'risked_investments':risked_investments,
            'time_deposit':time_deposit,
            'savings_interest':savings_interest
        }
        return Response(context)

class UserInvestmentUpload(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserInvestmentUploadSerializer

    def post(self, request, user_id):
        user_id = Insuree.objects.get(user_id = user_id)
        investment_type = CompanyInvestmentType.objects.get(id = request.data.get('investment_type'))
        insureePolicy_id = InsureePolicy.objects.get(id = request.data.get('user_policy_id'))
        initial_deposit = request.data.get('initial_deposit')
        succeeding_deposit = request.data.get('succeeding_deposit')
        number_of_years_to_pay = request.data.get('number_of_years_to_pay')

        risk_rate = investment_type.risk_rate
        partial_investment_value = initial_deposit + (succeeding_deposit * number_of_years_to_pay)
        risk_rated_investment = round(partial_investment_value * (1+( risk_rate * number_of_years_to_pay)), 2)
        investment_refno = generate_transaction_id()

        user_investment = UserInvestment.objects.create(
            userpolicy_Id = insureePolicy_id, 
            investor_id = user_id,
            investment_type = investment_type,
            available_investment_interval = 'Annual',
            initial_dep = initial_deposit,
            succ_dep_amount = succeeding_deposit,
            number_of_yearspayment = number_of_years_to_pay,
            partial_value= partial_investment_value,
            future_value = risk_rated_investment,
            investment_refno = investment_refno,
            created_at = datetime.today()
        )

        # send_investment_confirmation.delay(user_id, user_investment)

        response = {
            'message':'Investment successfully created!!',
            'investment_refno':investment_refno
        }
        return Response(response)


class GetCompanyInvestmentType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CompanyInvestmentTypeSerializer

    def get_queryset(self):
        company_req_id = self.kwargs['company_id']
        return Investment.CompanyInvestmentType.objects.filter(company = company_req_id)

class GetUserInvestmentStatus(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = GetUserInvestmentSerializer

    def get_queryset(self):
        insuree_id = self.kwargs['insuree_id']
        return UserInvestment.objects.filter(investor_id = insuree_id)

class GetListOfUserInvestment(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_investment = UserInvestment.objects.all().values(
            'id',
            'investor_id',
            #'investor_id__insuree',
            'investment_type',
            'created_at',
            'investment_status'
        ).annotate(policy_holder=Concat(
                'investor_id__first_name',
                V(' '), 'investor_id__last_name', V(''),
                output_field=CharField()
                ))
        
        context = {
            "user_investment": user_investment,
        }

        return Response(context)

        """
        Choices are: available_investment_interval, created_at, 
        future_value, id, initial_dep, investment_refno, 
        investment_status, investment_type, investment_type_id, 
        investor_id, investor_id_id, number_of_yearspayment, 
        partial_value, succ_dep_amount, userpolicy_Id, 
        userpolicy_Id_id
        """

class UploadInvestmentProduct(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CompanyInvestmentTypeSerializer
    def post(self, request):
        serializer = CompanyInvestmentTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)