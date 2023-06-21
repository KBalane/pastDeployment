from rest_framework import serializers
from digiinsurance.models.Investment import CompanyInvestmentType, UserInvestment

__all__ = ['CompanyInvestmentTypeSerializer', 'UserInvestmentSerializer', 'UserInvestmentUploadSerializer',
           'GetUserInvestmentSerializer']


class CompanyInvestmentTypeSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField()
    investment_name = serializers.CharField()
    invest_description = serializers.CharField()
    risk_rate = serializers.FloatField()
    investment_term = serializers.CharField()
    income_bracket = serializers.DecimalField(max_digits=20, decimal_places=2, default=0)
    risk_tolerance = serializers.CharField()
    other_information = serializers.CharField()
    product_image = serializers.ImageField()
    facts_sheet = serializers.FileField()

    class Meta:
        model = CompanyInvestmentType
        fields = ('company_id', 'investment_name', 'invest_description', 'risk_rate', 'investment_term',
                  'income_bracket', 'risk_tolerance', 'other_information', 'product_image', 'facts_sheet')


class UserInvestmentSerializer(serializers.ModelSerializer):
    initial_dep = serializers.IntegerField()
    succ_dep_amount = serializers.IntegerField()
    end_year_payment = serializers.IntegerField()
    company_id = serializers.IntegerField()

    class Meta:
        model = UserInvestment
        fields = ('initial_dep', 'succ_dep_amount', 'end_year_payment', 'company_id')


class UserInvestmentUploadSerializer(serializers.ModelSerializer):
    user_policy_id = serializers.IntegerField()
    investment_type = serializers.IntegerField()
    initial_deposit = serializers.IntegerField()
    succeeding_deposit = serializers.IntegerField()
    number_of_years_to_pay = serializers.IntegerField()

    class Meta:
        model = UserInvestment
        fields = ('user_policy_id', 'investment_type', 'initial_deposit', 'succeeding_deposit',
                  'number_of_years_to_pay')


class GetUserInvestmentSerializer(serializers.ModelSerializer):
    partial_value = serializers.IntegerField()

    class Meta:
        model = UserInvestment
        fields = ('partial_value',)
