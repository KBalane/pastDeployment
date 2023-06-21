from cocolife.serializers import AgentAssistedSerializer
from cocolife.models import AgentAssisted

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

__all__ = ['AgentAssisted']

class AgentAssisted(ListCreateAPIView):
    # TODO - Make Authenticated
    permission_classes = (AllowAny,)
    queryset = AgentAssisted.objects.all()
    serializer_class = AgentAssistedSerializer

