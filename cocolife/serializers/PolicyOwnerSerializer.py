from rest_framework import serializers
from cocolife.models.PolicyOwner import PolicyOwner


class PolicyOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyOwner
        fields = '__all__'
