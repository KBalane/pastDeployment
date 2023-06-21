from rest_framework.response import Response
from rest_framework.views import APIView

from cocolife.serializers import ProductInsureeSerializer

from cocolife.models.Beneficiary import Beneficiary
from cocolife.models.ProductInsuree import ProductInsuree
from cocolife.models.DigiInsuree import DigiInsuree
from cocolife.models.DigiTransaction import DigiTransaction
from cocolife.models.Product import Benefit, Product

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

__all__ = ['ProductInsureeCreate', 'ProductInsureeUpdate', 'ProductInsureeList']


class ProductInsureeCreate(ListCreateAPIView):
    # TODO - Make Authenticated
    permission_classes = (AllowAny,)
    queryset = ProductInsuree.objects.all()
    serializer_class = ProductInsureeSerializer

    # def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs) super().create(
    # request, *args, **kwargs) id = serializer.data['id'] cursor = connection.cursor() cursor.execute(""" Select
    # Ben.face_amount from digiinsurance.cocolife_benefit as Ben join digiinsurance.cocolife_variant as Var on Ben.id
    # = 1 and Var.id = %s; """, [id]) face_amount = cursor.fetchall() region | this code is for assigning to agent
    # assisted if not ipa // working uncomment if need automatic assign from product summary/ prodinsuree billed_to =
    # request.data.get('billed_to') user = CocoInsuree.objects.get(user = billed_to) product_id = request.data.get(
    # 'billed_to') product = Product.objects.get(id = product_id) if(product != 1): assist =
    # AgentAssisted.objects.create( user = user, datetime = datetime.now(), product = product )"face_amount":
    # "facemount from benef" assist.save() return Response('200') else: return Response('200') endregion


class ProductInsureeUpdate(RetrieveUpdateDestroyAPIView):
    # TODO - Make Authenticated
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    queryset = ProductInsuree.objects.all()
    serializer_class = ProductInsureeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        user = DigiInsuree.objects.filter(user=serializer.data['billed_to']).values()[0]
        product = Product.objects.filter(id=serializer.data['product']).values()[0]
        beneficiaries = Beneficiary.objects.filter(product_insuree=serializer.data['id']).values('full_name')
        benefit_qs = Benefit.objects.filter(variant=serializer.data['variant']).values('name', 'face_amount')
        benefits = sorted(benefit_qs, key=lambda x: x['face_amount'], reverse=True)
        # validate
        payment_details = DigiTransaction.objects.filter(productinsuree=serializer.data['id']).values()

        if not payment_details:
            return Response({"error:": "No Payment Found"}, status=401)

        benef_arr = []
        for item in beneficiaries:
            benef_arr.append(item['full_name'])

        context = {
            # Sumary Fields
            "product": product['name'],
            "face_amount_max": '{:.2f}'.format(benefits[0]['face_amount']),
            "billed_to": '%s %s' % (user['first_name'], user['last_name']),
            "beneficiaries": benef_arr,
            "paid_using": payment_details[0]['processor'],
            "payment_term": serializer.data['payment_term'],
            "total_amount": serializer.data['premium_amount_due'],

            # Addifional Fields for Specific Product Insuree
            "due_date": serializer.data['premium_due_date'],
            "policy_duration": {
                "start": serializer.data['created_at'],
                "end": instance.get_expiration_date()
            },
            "full_benefits": benefits
        }

        return Response(context)


class ProductInsureeList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id_search):
        queryset = ProductInsuree.objects.all().values('id', 'product__name', 'package__name', 'status', 'payment_term',
                                                       'premium_amount_due', 'premium_due_date').filter(
            billed_to_id=id_search)
        return Response(queryset)
