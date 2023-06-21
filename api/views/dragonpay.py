import logging

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from django_dragonpay.constants import DRAGONPAY_PAYMENT_METHODS
from django_dragonpay.forms import *
from django_dragonpay.models import DragonpayTransaction, DragonpayPayout
# from django_dragonpay.api.soap import split_payments

from rest_framework import viewsets
from rest_framework.response import Response

# from api.tasks import send_payout_receipt
# from apptitude.models.classes import Class
# from apptitude.models.course import Course
from digiinsurance.models import Transaction

# from coupons.models import CouponPayment

logger = logging.getLogger('dragonpay')

__all__ = [
    'dragonpay_postback',
    'DragonpayProcessorViewSet',
    'dragonpay_payout_postback'
    ]


@csrf_exempt
def dragonpay_postback(request):
    form = DragonpayCallbackForm(request.POST or request.GET)

    if not form.is_valid():
        if not settings.DRAGONPAY_TEST_MODE:
            if request.method == 'POST':
                return HttpResponse('result=FAIL_DIGEST_MISMATCH')
            # TODO redirect to failed payment page for dragonpay redirect
            # else:
            #     return redirect('dashboard:dashboard')

    if settings.DRAGONPAY_SAVE_DATA:
        try:
            txn = DragonpayTransaction.objects.get(
                id=form.cleaned_data['txnid'])

        except DragonpayTransaction.DoesNotExist as e:
            logger.error('Dragonpay transaction does not exist', e)
            raise e
        else:
            # update the status of the transaction
            txn.status = form.cleaned_data['status']
            refno = form.cleaned_data['refno']

            # insuree = Insuree.objects.get(email=txn.email)
            if request.method == 'POST':
                # Fetch and complete the Payment Details Object
                transaction = Transaction.objects.get(txn_id=txn.id)
                transaction.complete()

            # set the reference number if it is still null
            if not txn.refno:
                txn.refno = refno

            txn.save(update_fields=['status', 'refno'])

    # if request.method == 'POST':
    #TODO: create a payment successful page to redirect to  
    response_html = 'Payment Successful! Reference Number: <b class="ref_num">%s</b>' % (refno)
    return HttpResponse(response_html)


@csrf_exempt
def dragonpay_payout_postback(request):
    form = DragonpayPayoutCallbackForm(
        request.POST or request.GET)

    if not form.is_valid():
        if not settings.DRAGONPAY_TEST_MODE:

            if request.method == 'POST':
                return HttpResponse('result=FAIL_DIGEST_MISMATCH')
            # TODO redirect to failed payment page for dragonpay redirect
            # else:
            #     return redirect('dashboard:dashboard')

    if settings.DRAGONPAY_SAVE_DATA:
        try:
            txn = DragonpayPayout.objects.get(
                id=form.cleaned_data['merchanttxnid'])
            batch = BatchPayout.objects.get(
                txn_id=form.cleaned_data['merchanttxnid'])
        except DragonpayPayout.DoesNotExist as e:
            logger.error('Dragonpay/Batch transaction does not exist', e)
            raise e
        else:
            # update the status of the transaction
            txn.status = form.cleaned_data['status']

            if txn.status == 'S':
                batch.complete()
                if request.method == 'GET':
                    send_payout_receipt.delay(batch.id, txn.id)

            # set the reference number if it is still null
            if not txn.refno:
                txn.refno = form.cleaned_data['refno']

            txn.save(update_fields=['status', 'refno'])

    if request.method == 'POST':
        return HttpResponse('result=OK')
    else:
        return redirect('dashboard:dashboard')


class DragonpayProcessorViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(DRAGONPAY_PAYMENT_METHODS)
