from decimal import Decimal
import logging
import urllib
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_dragonpay.api.soap import get_txn_url_from_token, get_txn_token
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
from digiinsurance.models import Transaction

logger = logging.getLogger('api.views')

__all__ = ['Dragonpay_redirect_payment']


class Dragonpay_redirect_payment(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        if not user.insuree:
            return Response({'detail': 'This account is not allowed to register for insurance policies'},
                            status=status.HTTP_400_BAD_REQUEST)
        insuree = user.insuree

        if not user.is_verified:
            return Response({'detail': 'This account is not yet verified'}, status=status.HTTP_400_BAD_REQUEST)

        if 'insuree_policy_id' in request.data:
            enrolled_object = InsureePolicy.objects.get(id=request.data.get('insuree_policy_id'))
            print(enrolled_object)
            insuree_policy = enrolled_object
            pay_amount = enrolled_object.premium_amount_due
            # vat = enrolled_object.tax
            vat = 0  # set tax as 0 for testing
        else:
            raise Http404('Insuree Policy object missing.')

        company = enrolled_object.policy.company
        action = request.data.get('action')

        if action in ['otc_bank', 'online_bank', 'others']:
            insureePolicy_id = insuree_policy.id
            proc_id = request.data.get(action)
            proc_type = action
            insureePolicy = insuree_policy
            insuree = insuree_policy.insuree
            fee = Decimal('20.00')
            vat = vat
            amount = pay_amount + fee

            if hasattr(insureePolicy, 'loan'):
                payment_type = Transaction.LOAN_PAYMENT
            else:
                payment_type = Transaction.FULL_PAYMENT

            insuree_policy_name = insuree_policy.policy.name
            trunc = (insuree_policy_name[:75] + '...') if len(insuree_policy_name) > 75 else insuree_policy_name
            description = "%s Payments for %s, PHP %s" % (insuree.email, trunc, amount)
            email = insuree.email

            txn_id, token = get_txn_token(
                amount=amount,
                description=description,
                email=insuree.email
            )

            txn_url = get_txn_url_from_token(token, proc_id=proc_id)

            payment = Transaction.objects.create(
                insuree=insuree,
                insureePolicy=insuree_policy,
                company=company,
                txn_id=generate_transaction_id(),
                amount=amount,
                vat=vat,
                channel=Transaction.DRAGONPAY,
                payment_type=Transaction.FULL_PAYMENT,
                processor=proc_id,
                processor_type=proc_type,
                description=description
            )
            payment.complete()

            return Response(txn_url, status=status.HTTP_200_OK)
