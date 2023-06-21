from rest_framework import serializers

from cocolife.models import AgentAssisted

__all__ = ['AgentAssistedSerializer']

class AgentAssistedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentAssisted
        fields = ('__all__')