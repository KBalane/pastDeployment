
from cocolife.models import CompanyInformation
from cocolife.serializers import CompanyInformationSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

__all__ = ['CompanyInformation']

class CompanyInformation(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = CompanyInformation.objects.all()
    serializer_class = CompanyInformationSerializer




