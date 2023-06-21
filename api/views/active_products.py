from digiinsurance.models import InsureePolicy
from digiinsurance.models import Policy
from digiinsurance.models import Company

from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.InsureeSerializer import InsureeSerializer
# from api.serializers import ActiveProductsSerializer
from django.db.models import Count
from rest_framework.permissions import AllowAny

__all__ = ['Active_Products', 'MostPopularProducts']


class Active_Products(APIView):
    permission_classes = [AllowAny]
    serializer_class = InsureeSerializer

    def get(self, request):
        insuree_id = InsureePolicy.objects.all().values_list('insuree')
        active_products = InsureePolicy.objects.all().values(
            'policy', 'policy__name', 'policy__description', 'status'
        ).filter(status='Active').annotate(active_users=Count('status'))  # insuree = 44 / 44 should be current user

        active_products_count = active_products.filter(status='active').count()  # , insuree = 44 comma represents and

        context = {
            "active_products": active_products,
            "active_products_count": active_products_count
        }
        return Response(context)


class MostPopularProducts(APIView):
    """Displays the Most Popular Products (Based on the most availed products)"""
    permission_classes = [AllowAny]
    serializer_class = InsureeSerializer

    def get(self, request):
        most_popular = InsureePolicy.objects.all().values(
            'policy', 'policy__name', 'policy__description', 'policy__icon_file').filter(
            status='Active').annotate(active_users=Count('status')).order_by('-active_users')[:5]

        context = {
            "most_popular_products": most_popular
        }
        return Response(context)
