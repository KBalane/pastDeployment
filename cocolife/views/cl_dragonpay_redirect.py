from decimal import Decimal

from django_dragonpay.api.soap import get_txn_url_from_token, get_txn_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import generate_transaction_id

from digiinsurance.models.User import User

from cocolife.models.ProductInsuree import ProductInsuree
from cocolife.models.DigiTransaction import DigiTransaction
from cocolife.serializers.DigiTransactionSerializer import CLPaymentSerializer

from django.http import Http404

__all__ = ['CLDragonpay_redirect_payment']


class CLDragonpay_redirect_payment(APIView):
    queryset = DigiTransaction.objects.all()
    serializer_class = CLPaymentSerializer

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        # if not user.insuree:
        #     return Response(
        #         {'detail': 'This account is not allowed to register for insurance policies'},
        #         status=status.HTTP_400_BAD_REQUEST)
        # insuree = user.insuree

        # if not user.is_verified:
        #     return Response(
        #         {'detail': 'This account is not yet verified'},
        #         status=status.HTTP_400_BAD_REQUEST)

        if 'productInsuree' in request.data:
            enrolled_object = ProductInsuree.objects.get(
                id=request.data.get('productInsuree'))
            print(enrolled_object)
            product_insuree = enrolled_object
            pay_amount = enrolled_object.premium_amount_due
            # vat = enrolled_object.tax
            vat = 0  # set tax as 0 for testing
        else:
            raise Http404('Insuree Policy object missing.')

        # company = enrolled_object.policy.company
        action = request.data.get('action')

        if action in ['otc_bank', 'online_bank', 'others']:
            product_insuree_id = product_insuree.id
            proc_id = request.data.get(action)
            proc_type = action
            productInsuree = product_insuree
            cocoinsuree = product_insuree.billed_to
            fee = Decimal('20.00')
            vat = vat
            amount = pay_amount + fee

            if hasattr(productInsuree, 'loan'):
                payment_type = DigiTransaction.LOAN_PAYMENT
            else:
                payment_type = DigiTransaction.FULL_PAYMENT

            insuree_policy_name = product_insuree.product.name
            trunc = (insuree_policy_name[:75] + '...') if len(insuree_policy_name) > 75 else insuree_policy_name
            description = "%s Payments for %s, PHP %s" % (cocoinsuree.email, trunc, amount)
            email = cocoinsuree.email

            txn_id, token = get_txn_token(
                amount=amount,
                description=description,
                email=cocoinsuree.email)

            txn_url = get_txn_url_from_token(token, proc_id=proc_id)

            payment = DigiTransaction.objects.create(
                cocoinsuree=cocoinsuree,
                productinsuree=product_insuree,
                # company=company,
                txn_id=generate_transaction_id(),
                amount=amount,
                # vat=vat,
                channel=DigiTransaction.DRAGONPAY,
                payment_type=DigiTransaction.FULL_PAYMENT,
                processor=proc_id,
                processor_type=proc_type,
                # description= description
            )
            payment.complete()

            # update invoice once payment is fulfilled
            obj = ProductInsuree.objects.get(id=request.data.get('productInsuree'))
            obj.update_due_date()

            context = {
                "txn_url": txn_url,
                "txn_id": payment.txn_id
            }

            return Response(context, status=status.HTTP_200_OK)
