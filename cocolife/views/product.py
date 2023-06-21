from rest_framework.views import APIView

from cocolife.serializers.ProductSerializer import CreateProductSerializer, ProductSerializer
from cocolife.serializers.PolicyOwnerSerializer import PolicyOwnerSerializer
from cocolife.serializers.UnderwriterSerializer import UnderwriterSerializer
from cocolife.serializers.DigiInsureeSerializer import DigiInsureeSerializer

from cocolife.models import DigiInsuree, ProductInsuree
from cocolife.models.Product import Product
from cocolife.models.Underwriting import Underwriting

from rest_framework import status
from rest_framework.generics import (RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
import json

__all__ = ['Products', 'Underwriter', 'ProductByID', 'ProductCreate', 'PurchaseProduct', 'ProductLikeinfo',
           'like_product', 'ProductDetailed']


class Products(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     #query products by category
    #     qs = super().get_queryset()
    #     type = self.request.query_params.get('category')
    #     if type:
    #         qs = qs.filter(category=type)
    #     return qs
    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.request.user.is_authenticated:
            context['user_id'] = self.request.user.pk

        return context


class ProductCreate(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer


class ProductByID(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class Underwriter(RetrieveUpdateAPIView):
    # permission_classes=(AllowAny,) #TODO - Authenticate.
    lookup_field = 'pk'
    queryset = Underwriting.objects.all()
    serializer_class = UnderwriterSerializer

    # #LOG FOR UNDERWRITING
    # def get_queryset(self):
    #     from cocolife import utils
    #     utils.coco_user_log(self.__class__.__name__,self.request.user)
    #     return super().get_queryset()


# UNDERWRITER STATUS VIEW LAHAT THEN MAY FILTER

class PurchaseProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user  # Returns First and Last name of User
        name_from_req = ('%s %s' % (request.data['first_name'], request.data['last_name']))  # name from request

        if user.get_full_name() == name_from_req:
            insuree = DigiInsuree.objects.get(user=user.id)
            serializer = DigiInsureeSerializer(insuree, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PolicyOwnerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                ProductInsuree.objects.filter(pk=request.data['product_insuree']).update(is_self_insured=False)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductLikeinfo(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        likes_per_prod = Product.objects.all().values(
            'id', 'name'
        ).annotate(like_count=Count('liked'))
        context = {
            # "product": serializer.data(),
            'ListofProducts_like': likes_per_prod
        }
        return Response(context)


class ProductDetailed(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, product_id):
        queryset = Product.objects.all().filter(id=product_id).values('id', 'name', 'description')
        like_count = Product.objects.all().filter(id=product_id).values(
            'id', 'liked'
        ).filter(id=product_id).aggregate(like_count=Count('liked'))
        serializer = ProductSerializer(queryset, many=True)
        context = {
            # "products": serializer.data,  #all data
            "products": queryset,
            "like_count": like_count
        }
        return Response(context)


@csrf_exempt
@api_view(["GET", "POST", "PUT"])
@permission_classes([AllowAny])
def like_product(request, product_id, user_id):
    data = ""
    post = get_object_or_404(Product, id=product_id)

    if post.liked.filter(user_id=user_id).exists():
        post.liked.remove(user_id)
        data = "Unliked"
    else:
        post.liked.add(user_id)
        data = "Liked"
    post.save()
    return Response(data)
