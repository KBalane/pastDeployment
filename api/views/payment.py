from decimal import Decimal
import json
from django_dragonpay.forms import DragonpayCallbackForm
import logging
import urllib
from datetime import date, datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_dragonpay.api.soap import get_txn_token_url
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView

# from api.serializers import EnrollmentSerializer
from api.utils import generate_transaction_id

from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.User import User
from digiinsurance.models.Insuree import Insuree
from digiinsurance.models.Transaction import Transaction

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

# from django_dragonpay.api.soap import get_txn_url_from_token, get_txn_token, get_txn_token_url

from magpy.api.charge import Charge
from magpy.api.token import Token

from api.serializers.TransactionSerializer import TransactionSerializer, PaymentSerializer
from django_dragonpay.models import DragonpayTransaction

logger = logging.getLogger('api.views')

__all__ = ['PaymentView', 'PaymentView2', 'GetTransactionRefNo', 'GetDragonPayTransactionRefNo']

MAGPIE_FEE = 0.039


class PaymentView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, user_id):
        list_of_payments = Transaction.objects.all().values(
            'txn_id',
            'insuree__first_name',
            'insuree__middle_name',
            'insuree__last_name',
            'transaction_date',
            'amount',
            'payment_type',
            'channel',
            'insureePolicy__status',
            'insuree')

        list_of_payments = list_of_payments.filter(insuree=user_id)

        return Response(list_of_payments)

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        if not user.insuree:
            return Response(
                {'detail': 'This account is not allowed to register for insurance policies'},
                status=status.HTTP_400_BAD_REQUEST)
        insuree = user.insuree

        if not user.is_verified:
            return Response(
                {'detail': 'This account is not yet verified'},
                status=status.HTTP_400_BAD_REQUEST)

        if 'insuree_policy_id' in request.data:
            enrolled_object = InsureePolicy.objects.get(
                id=request.data.get('insuree_policy_id'))
            print(enrolled_object)
            insuree_policy = enrolled_object
            pay_amount = enrolled_object.premium_amount_due
            # vat = enrolled_object.tax
            vat = 0  # set tax as 0 for testing
        else:
            raise Http404('Insuree Policy object missing.')

        company = enrolled_object.policy.company
        action = request.data.get('action')

        data = {
            'date_insured': timezone.now(),
            'status': InsureePolicy.NOTPAID
        }
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

        if action in ['otc_bank', 'online_bank', 'others']:
            proc_id = request.data.get(action)
            fee = Decimal('20.00')
            total_amount = pay_amount + fee
            params = {
                'insuree_policy_id': insuree_policy.id,
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

        elif action == 'card':
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
                description='Payment for %s' % insuree_policy,
                statement_descriptor='DigiInsurance',
            )
            # print("CHARGE CREATED")
            # print(results)

            if results['status'] == 'succeeded':
                insuree_policy.status = InsureePolicy.PAID
                insuree_policy.save(update_fields=['status'])
                payment = Transaction.objects.create(
                    insuree=insuree,
                    insureePolicy=insuree_policy,
                    company=company,
                    txn_id=results['id'],
                    amount=total_amount,
                    fee=0,
                    vat=vat,
                    channel=Transaction.MAGPIE,
                    payment_type=Transaction.FULL_PAYMENT,
                    processor_type=Transaction.CARD,
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
            payment = Transaction.objects.create(
                # enrollment=enrollment,
                txn_id=generate_transaction_id(),
                amount=pay_amount,
                vat=vat,
                payment_type=Transaction.FULL_PAYMENT,
                school=school,
                channel=Transaction.CASH,
                processor='CASH',
                processor_type=Transaction.CASH
            )

        transac_id = Transaction.objects.all().values_list('txn_id').order_by('-created_at')

        context = {
            'success': 'Payment Successful',
            "txn_id": transac_id[0][0]
        }

        return Response(context, status=status.HTTP_200_OK)

        # if not object_type:
        #     return Response({'detail': 'Object type not found'}, status=status.HTTP_400_BAD_REQUEST)
        # if not object_id:
        #     return Response({'detail': 'Object ID not found'}, status=status.HTTP_400_BAD_REQUEST)
        # if not isinstance(object_id, int):
        #     return Response({'detail': 'Object ID should be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        # # Make sure request is specifying zero for initial amount to be paid to prevent irresonsible requests
        # if not pay_amount and pay_amount != 0:
        #     return Response({'detail': 'Please specify pay_amount'}, status=status.HTTP_400_BAD_REQUEST)
        # # Get Course or Class
        # try:
        #     if object_type == 'course':
        #         enroll_object = Course.objects.get(id=object_id)

        #     elif object_type == 'class':
        #         enroll_object = Class.objects.get(id=object_id)

        #     else:
        #         return Response({'detail': 'Invalid Object type'}, status=status.HTTP_400_BAD_REQUEST)
        # except ObjectDoesNotExist as e:
        #     return Response({'detail': 'Object not found'}, status=status.HTTP_400_BAD_REQUEST)
        # if enroll_object.fee == 0:
        #     return Response({'detail': 'Object has no fee'}, status=status.HTTP_400_BAD_REQUEST)

        # if pay_amount >= enroll_object.fee:
        #     return Response({'detail': 'Might as well Enroll already'}, status=status.HTTP_400_BAD_REQUEST)

        # ct = ContentType.objects.get_for_model(enroll_object)

        # if Enrollment.objects.filter(content_type=ct, object_id=enroll_object.id,
        #                              student=user.student):
        #     return Response({'detail': 'User already enrolled'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        # # Create Enrollment Object

        # # e = Enrollment.objects.create(
        # #     enrolled_object=enroll_object,
        # #     student=user.student,
        # #     date_enrolled=timezone.now(),
        # #     status=Enrollment.NOTPAID)

        # Loan.objects.create(
        #     enrollment=e,
        #     student=user.student,
        #     principal=enroll_object.fee,
        #     outstanding=enroll_object.fee,
        #     total=enroll_object.fee
        # )

        # if pay_amount == 0:
        #     return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
        # else:
        #     redirect_url = '%sdragonpay_redirect/%s/%s/%s' % (
        #         settings.WEB_APP_URL, enroll_object.school.domain,
        #         object_type, id)
        #     return Response({
        #         'detail': 'redirect',
        #         'redirect_url': redirect_url
        #     }, status=status.HTTP_200_OK)


class PaymentView2(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request):
        list_of_payments = Transaction.objects.all().values(
            'txn_id',
            'insuree__first_name',
            'insuree__middle_name',
            'insuree__last_name',
            'transaction_date',
            'amount',
            'payment_type',
            'channel',
            'insureePolicy__status',
            'insureePolicy__policy',
            'insuree')

        return Response(list_of_payments)


class GetTransactionRefNo(APIView):
    def get(self, request, insureePolicy):
        try:
            query = Transaction.objects.all().values_list(
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


class GetDragonPayTransactionRefNo(APIView):
    def get(self, request, txn_id):
        query = Transaction.objects.all().values_list(
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
