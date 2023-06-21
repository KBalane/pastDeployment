from api.serializers.PolicySerializer import PolicySerializer
from api import serializers
from digiinsurance.models import PolicyCalculator as PC, Policy, PolicyRequirements
from api.serializers import GetAllPolicySerializer, GetPolicyBenefitsSerializer

from api.serializers import PolicyCalculatorSerializer, PolicyRequirementsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from decimal import Decimal
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from django.db import connection

__all__ = ['PolicyCalculate','GetPolicyCalculator','PolicyCalculateV2','test_extract_base_sum_assured','PolicyRequirementsCreate','PolicyRequirementsList'] #,'PolicyCalculatorUpdate']

"""
class PolicyCalculate(APIView):
    def get(self, request, user_id, policy_id):
        base_sum_assured = Policy.objects.values_list('benefits').filter(id = policy_id)
        
        clean_sum_assured = str(base_sum_assured[0][0][0]).split("'") # this gets the base sum assured and splits the variable and data
        
        context = {
            'base_sum_assured' : clean_sum_assured[7],
            #'annual_premium' : annual_premium
        }

        return Response(context)
"""

def calculateBaseSumAssured(gender, discount, coverage_amount, policy_term_length, life_insurance_interest):
        if "F" in str(gender[0][0]):
            discount = 0.3
            sum_assured_of = discount * (coverage_amount[0][0] * policy_term_length[0][0] * Decimal(life_insurance_interest))
        else:
            sum_assured_of = (coverage_amount[0][0] * policy_term_length[0][0] * Decimal(life_insurance_interest))
        
        return sum_assured_of

def calculateAnnualPremium(gender, discount, coverage_amount, annual_premium, life_insurance_interest):
        if "F" in str(gender[0][0]):
            discount = 0.3
            annual_premium = discount * (coverage_amount[0][0] * annual_premium[0][0] * Decimal(life_insurance_interest))
        else:
            annual_premium = (coverage_amount[0][0] * annual_premium[0][0] * Decimal(life_insurance_interest))
        
        return annual_premium

def showPolicies(base_sum_assured):
    
    #queryset = Policy.objects.filter(benefits__name__2='sample title')
    '''
    JSON_EXTRACT(packages,'$[0].base_price')
    cursor.execute("""
    SELECT * FROM digiinsurance.digiinsurance_policy 
    WHERE JSON_UNQUOTE(JSON_EXTRACT(packages,'$[0].base_price')) 
    <= '%s';""", [base_sum_assured])
    '''
    cursor = connection.cursor()
    cursor.execute("""
    SELECT id,name,description,category,
    packages->'$[0].base_price',
    packages->'$[1].base_price',
    packages->'$[2].base_price'
    FROM digiinsurance.digiinsurance_policy 
    WHERE JSON_EXTRACT(packages,'$[0].base_price')
    <= %s OR JSON_EXTRACT(packages,'$[1].base_price')
    <= %s OR JSON_EXTRACT(packages,'$[2].base_price')
    <= %s 
    ;""", [base_sum_assured,base_sum_assured,base_sum_assured])


    recommended_policies = cursor.fetchall()
    return recommended_policies



class PolicyCalculate(APIView):

    def get(self, request, user_id, policy_id):
        gender = PC.objects.values_list(
            'user__insuree__gender').filter(user__id = user_id)
        life_insurance_interest = 0.045 
        discount = 0.3 # women could pay up to 30% less than men
        policy_term_length = PC.objects.values_list('policy_length').filter(Q(user__id = user_id) & Q(policy__id = policy_id))
        coverage_amount = Policy.objects.values_list('price').filter(id=policy_id)
        annual_premium = PC.objects.values_list('annual_premium').filter(Q(user__id = user_id) & Q(policy__id = policy_id))
        
        
        sum_assured_of = calculateBaseSumAssured(gender, discount, coverage_amount, policy_term_length, life_insurance_interest)
        annual_premium = calculateAnnualPremium(gender, discount, coverage_amount, annual_premium, life_insurance_interest)
        

        context = {
            'policy_id':policy_id,
            'base_sum_assured_basic':sum_assured_of,
            'annual_premium_basic': annual_premium,

            'base_sum_assured_standard':sum_assured_of,
            'annual_premium_standard': annual_premium,

            'base_sum_assured_lite':sum_assured_of,
            'annual_premium_lite': annual_premium,

            'base_sum_assured_pro':sum_assured_of,
            'annual_premium_pro': annual_premium,

        }
        #base, standard, lite, pro
        return Response(context)


class PolicyCalculateV2(APIView):
    """
    Calculates the current savings, current investments, 
    insurance coverage, household expenses, and liabilities.

    Displays the recommended coverage, base sum assured and annual premium.
    """


    def get(self, request,policy_id,current_savings, current_investments, insurance_coverage, household_expenses, liabilities):
        
        base_sum_assured = (current_savings + current_investments + insurance_coverage) - (household_expenses + liabilities)
        recommended_coverage = base_sum_assured * 10.00
        annual_premium = base_sum_assured / 10.00
        query = Policy.objects.all().filter(id=policy_id)
        serializer = GetPolicyBenefitsSerializer(query, many=True)

        context = {
            "recommended_coverage": recommended_coverage,
            "base_sum_assured_basic": base_sum_assured,
            "annual_premium_basic": annual_premium,

            #basic,standard, lite and pro values to be updated
            'base_sum_assured_standard':round((base_sum_assured * 0.2), 2),
            'annual_premium_standard': round((annual_premium *0.2), 2),

            'base_sum_assured_lite':round((base_sum_assured *0.1), 2),
            'annual_premium_lite': round((annual_premium *0.1), 2),

            'base_sum_assured_pro':round((base_sum_assured *0.4), 2),
            'annual_premium_pro': round((annual_premium *0.4), 2),

            #'benefits':serializer.data,
            "recommended_policies" : showPolicies(base_sum_assured),
        }
        #base, standard, lite, pro
        return Response(context)


        #optional feature: displays the recommended policies based on the calculation
        # using showPolicies(base_sum_assured) method. Already working.

class GetPolicyCalculator(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = PC.objects.all()
    serializer_class = PolicyCalculatorSerializer

    def get_queryset(self):
        return super().get_queryset()
    
"""
class PolicyCalculatorUpdate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'
    queryset = PC.objects.all()
    serializer_class = PolicyCalculatorSerializer
"""

class test_extract_base_sum_assured(APIView):
    def get(self, request):
        query = Policy.objects.all().filter(benefits__contains = {'name':'Base sum assured','value':'2,795,001.00'})
        serializer = GetAllPolicySerializer(query, many=True)
        return Response(serializer.data)
    '''
    def get(self, request):
        #COMMENTED CODE IS WORKING
        #queryset = Policy.objects.filter(benefits__name__2='sample title')
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM digiinsurance.digiinsurance_policy 
        WHERE JSON_UNQUOTE(JSON_EXTRACT(benefits,'$[0].value')) 
        >= '120,000.00';""")

        recommended_policies = cursor.fetchall()

        context = {
            'recommended_policies': recommended_policies
        }
        #tepm = base_sum_assured_value
        return Response(context)
    '''

class PolicyRequirementsView(APIView):
    """
    Displays Policy Requirement Steps
    """
    def get(self, request):
        
        text = """Step 1: Enter your age
        The cost of life insurance increases 4.5-9% each year you put off buying coverage, based on policies offered by Policygenius in 2021. The younger you are, the lower your premiums, which is why it’s best to buy early if you’re able to.
        
        Step 2: Enter your gender
        Women could pay up to 30% less than men for the same amount of coverage on average, based on policies offered by Policygenius in 2021.
        
        Step 3: Choose your term length
        Your policy’s term length is how long your life insurance coverage lasts. Choose a term length that matches or exceeds your longest financial obligation (like your mortgage) so that your loved ones don’t end up liable for those costs.
        
        Step 4: Choose your coverage amount
        Policygenius advisers suggest buying coverage of 10-15 times your income, if not more. Even if you’re temporarily unemployed, you should get enough coverage to account for your anticipated future income."""
        return Response(text)
        
class PolicyRequirementsCreate(ListCreateAPIView):
    queryset = PolicyRequirements.objects.all()
    serializer_class = PolicyRequirementsSerializer

class PolicyRequirementsList(ListAPIView):
    #permission_classes = (AllowAny,)
    serializer_class = PolicyRequirementsSerializer
    
    def get_queryset(self):
        policy_req_id = self.kwargs['policy']
        return PolicyRequirements.objects.filter(policy = policy_req_id)
    


"""
Step 1: Enter your age
The cost of life insurance increases 4.5-9% each year you put off buying coverage, based on policies offered by Policygenius in 2021. The younger you are, the lower your premiums, which is why it’s best to buy early if you’re able to.
 
Step 2: Enter your gender
Women could pay up to 30% less than men for the same amount of coverage on average, based on policies offered by Policygenius in 2021.
 
Step 3: Choose your term length
Your policy’s term length is how long your life insurance coverage lasts. Choose a term length that matches or exceeds your longest financial obligation (like your mortgage) so that your loved ones don’t end up liable for those costs.
 
Step 4: Choose your coverage amount
Policygenius advisers suggest buying coverage of 10-15 times your income, if not more. Even if you’re temporarily unemployed, you should get enough coverage to account for your anticipated future income.
"""
