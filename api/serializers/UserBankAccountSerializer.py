from rest_framework import serializers

from digiinsurance.models.UserBankAccount import UserBankAccount
__all__ = ['UserBankAccountSerializer']


class UserBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankAccount
        # fields = ('id', 'first_name', 'middle_name', 'last_name')
        fields = '__all__'
