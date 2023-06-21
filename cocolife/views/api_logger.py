from cocolife.serializers.APILoggerSerializer import APILoggerSerializer
from cocolife.models.APILogger import APILogger

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination


__all__ = ['APILogger']


class APILoggerPaginator(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10


class APILogger(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = APILogger.objects.all().order_by('-created_at')
    serializer_class = APILoggerSerializer
    pagination_class = APILoggerPaginator
