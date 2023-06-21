from decimal import Decimal
import urllib
from datetime import date, datetime

from django.conf import settings
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from api.utils import generate_transaction_id

from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.User import User

from cocolife.models.DigiInsuree import DigiInsuree
from cocolife.models.ProductInsuree import ProductInsuree
from cocolife.models.DigiTransaction import DigiTransaction
from cocolife.serializers.DigiTransactionSerializer import CLPaymentSerializer

from django.http import Http404
from django.utils import timezone

from magpy.api.charge import Charge
from magpy.api.token import Token

from django_dragonpay.models import DragonpayTransaction

__all__ = ['CLPaymentBeta', 'CLPaymentView', 'CL_GetDragonPayTransactionRefNo']

MAGPIE_FEE = 0.039


class CLPaymentBeta(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = DigiTransaction.objects.all()
    serializer_class = CLPaymentSerializer


class CLPaymentView(APIView):
    permission_classes = (AllowAny,)
    queryset = DigiTransaction.objects.all()
    serializer_class = CLPaymentSerializer

    def get(self, request, user_id):
        list_of_payments = DigiTransaction.objects.all().values(
            'txn_id',
            'cocoinsuree__first_name',
            'cocoinsuree__middle_name',
            'cocoinsuree__last_name',
            'transaction_date',
            'amount',
            'payment_type',
            'channel',
            'productinsuree__status',
            'productinsuree__product__name',
            'cocoinsuree')

        list_of_payments = list_of_payments.filter(cocoinsuree=user_id)

        return Response(list_of_payments)

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        # if (user):
        #     print('working')
        #     print(user.id)
        # else:
        #     print('not working')

        # validations
        # if not user.insuree:
        #     return Response(
        #         {'detail': 'This account is not allowed to register for insurance policies'},
        #         status=status.HTTP_400_BAD_REQUEST)
        # cocoinsuree = user.cocoinsuree

        # if not user.is_verified:
        #     return Response(
        #         {'detail': 'This account is not yet verified'},
        #         status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        if 'productInsuree' in request.data:
            print('working')
            print('working')
            print('working')
            print('working')
            enrolled_object = ProductInsuree.objects.get(
                id=request.data.get('productInsuree'))
            print(enrolled_object)
            product_insuree = enrolled_object
            pay_amount = enrolled_object.premium_amount_due
            # vat = enrolled_object.tax
            vat = 0  # set tax as 0 for testing
        else:
            raise Http404('Insuree Policy object missing.')

        # company = enrolled_object.productinsuree.product.company
        action = request.data.get('action')

        data = {
            'date_insured': timezone.now(),
            'status': InsureePolicy.NOTPAID
        }
        # region check if payment done
        # Add check if payment already done
        # e = PaymentDetail.objects.filter(
        #     Q(course=course) | Q(class__course=course),
        #     student=request.user.student
        # )

        # if action in ['otc_bank', 'online_bank', 'others']:
        #     insureePolicy_id = insuree_policy.id
        #     proc_id = request.data.get(action)
        #     proc_type = action
        #     insureePolicy = insuree_policy
        #     insuree = insuree_policy.insuree
        #     fee = Decimal('20.00')
        #     vat = vat
        #     amount = pay_amount + fee

        #     if hasattr(insureePolicy, 'loan'):
        #         payment_type = Transaction.LOAN_PAYMENT
        #     else:
        #         payment_type = Transaction.FULL_PAYMENT

        #     # insuree_policy_name = .get_policy().name
        #     # trunc = (insuree_policy_name[:75] + '...') if len(insuree_policy_name)>75 else insuree_policy_name
        #     description = "%s Payments for sample Policy" % (amount)
        #     email = insuree.email

        #     txn_url = get_txn_token_url(
        #         amount, 
        #         description,
        #         email,
        #     )

        #     return Response(txn_url, status=status.HTTP_200_OK)

        #     if results['status'] == 'succeeded':
        #         insuree_policy.status=InsureePolicy.PAID
        #         insuree_policy.save(update_fields=['status'])
        #         payment=Transaction.objects.create(
        #             insuree=insuree,
        #             insureePolicy=insuree_policy,
        #             company=company,
        #             txn_id=results['id'],
        #             amount=total_amount,
        #             vat=vat,
        #             channel=Transaction.DRAGONPAY,
        #             payment_type=Transaction.FULL_PAYMENT,
        #             processor_type=action,
        #             processor=results['source']['brand'],
        #         )
        #         payment.complete()
        #     else:
        #         return Response({'detail':'Payment Failed'}, status=status.HTTP_400_BAD_REQUEST)

        #         return Response({
        #             'success': 'Payment Successful'
        #         }, status=status.HTTP_200_OK)
        # endregion

        if action in ['otc_bank', 'online_bank', 'others']:
            proc_id = request.data.get(action)
            fee = Decimal('20.00')
            total_amount = pay_amount + fee
            params = {
                'product_insuree_id': product_insuree.id,
                'amount': total_amount,
                'vat': vat,
                'fee': fee,
                'proc_id': proc_id,
                'proc_type': action
            }

            redirect_url = '%s/dragonpay_redirect/?%s' % (settings.WEB_APP_URL, urllib.parse.urlencode(params))

            return Response({
                'redirect_url': redirect_url
            }, status=status.HTTP_200_OK)

        elif action == 'card':  # Preferred RN
            token = Token()
            status_code, card_token = token.create(
                name=request.data.get("name"),
                number=request.data.get("number"),
                exp_month=request.data.get("exp_month"),
                exp_year=request.data.get("exp_year"),
                cvc=request.data.get("cvc"),
            )

            if status_code not in [200, 201]:
                return Response(card_token)
            # card_token = response
            # print("TOKEN CREATE SUCCESSFULL")
            # print(card_token)

            charge = Charge()
            # fee = (
            #     (pay_amount + Decimal('20.00')) / Decimal(1 - MAGPIE_FEE)
            # ).quantize(Decimal('.01')) - pay_amount
            # total_amount = pay_amount + fee
            total_amount = request.data.get('pay_amount')
            # print("amount="+total_amount)
            # print("source="+card_token['id'])
            # print("description="'Payment for %s' % insuree_policy)
            # print("statement_descriptor="'DigiInsurance')

            status_code, results = charge.create(
                amount=total_amount,
                source=card_token['id'],
                description='Payment for %s' % product_insuree,
                statement_descriptor='Cocolife',
            )
            # print("CHARGE CREATED")
            # print(results)

            if results['status'] == 'succeeded':
                # product_insuree.status = ProductInsuree.PAID
                # product_insuree.save(update_fields=['status'])
                payment = DigiTransaction.objects.create(
                    cocoinsuree=DigiInsuree.objects.get(user=user_id),
                    productinsuree=product_insuree,
                    txn_id=results['id'],
                    amount=total_amount,
                    # fee=0,
                    # vat=vat,
                    channel=DigiTransaction.MAGPIE,
                    payment_type=DigiTransaction.FULL_PAYMENT,
                    processor_type=DigiTransaction.CARD,
                    processor=results['source']['brand'],
                )
                payment.complete()

            else:
                return Response({
                    'detail': 'Payment Failed'
                }, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    'success': 'Payment Successful'
                }, status=status.HTTP_200_OK)


        elif action == 'cash':
            payment = DigiTransaction.objects.create(
                # enrollment=enrollment,
                txn_id=generate_transaction_id(),
                amount=pay_amount,
                vat=vat,
                payment_type=DigiTransaction.FULL_PAYMENT,
                # school=school,
                channel=DigiTransaction.CASH,
                processor='CASH',
                processor_type=DigiTransaction.CASH
            )

        transac_id = DigiTransaction.objects.all().values_list('txn_id').order_by('-created_at')

        # update product_insuree fields
        product_insuree.status = 'active'
        product_insuree.premium_last_paid = payment.amount
        product_insuree.update_due_date()
        product_insuree.save()

        context = {
            'success': 'Payment Successful',
            "txn_id": transac_id[0][0]
        }

        return Response(context, status=status.HTTP_200_OK)


class GetTransactionRefNo(APIView):
    def get(self, request, insureePolicy):
        try:
            query = DigiTransaction.objects.all().values_list(
                'txn_id',
                'created_at',
                'insureePolicy'
            ).filter(insureePolicy=insureePolicy).order_by('-created_at')
            context = {
                "ref_no": query[0][0],
                "date_created": query[0][1]
            }
            return Response(context)

        except IndexError:
            return Response("No existing transaction", status=404)


class CL_GetDragonPayTransactionRefNo(APIView):
    def get(self, request, txn_id):
        query = DigiTransaction.objects.all().values_list(
            'transaction_date'
        ).filter(txn_id=txn_id).order_by('-created_at')
        # get the transaction_date from query
        transaction_date = str(query[0][0])
        # split the milliseconds 2021-08-17 07:18:25.910000+00:00
        split_date = transaction_date.split(".")[0]
        # convert to a new format of date
        new_date = datetime.strptime(split_date, '%Y-%m-%d %H:%M:%S')
        # using the new_date to filter the dragonpayquery
        try:
            dragonpayquery = DragonpayTransaction.objects.all().values().filter(Q(created_at__contains=new_date))

            return Response(list(dragonpayquery))

        except IndexError:
            return Response("No existing transaction", status=404)

        # return Response(query)
