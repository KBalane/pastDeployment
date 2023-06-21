import logging
import os
import random
from decimal import Decimal

import requests
import string
from datetime import datetime
from io import BytesIO

# from pdfjinja import PdfJinja
# from pdf2image import convert_from_path

from django.conf import settings
# from django.core.files import File
# from django.http import Http404
# from django.urls import reverse
from rest_framework.authtoken.models import Token
from twilio.rest import Client
import facebook

# from dashboard.utils import generate_qrcode
from magpy.api import Charge

logger = logging.getLogger('api.utils')


def create_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


def generate_transaction_id(choices=string.ascii_uppercase + "345689"):
    """Transaction ID generator for PaymentTypeModel
    Transaction IDs may be used by users in interacting with payment
    gateways. Let us use uppercase and a few digits as choices to
    make it easier.
    """

    return ''.join([random.choice(choices) for i in range(10)])


class CSVWriter(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def create_magpie_charge(result, insureePolicy, quantity=1):
    MAGPIE_FEE = 0.039
    charge = Charge()
    amount = insureePolicy.total * quantity
    description = 'Payment for %s %s' % (quantity, insureePolicy.name)
    fee = (
                  (amount + Decimal('20.00')) / Decimal(1 - MAGPIE_FEE)
          ).quantize(Decimal('.01')) - amount
    status_code, results = charge.create(
        amount=amount + fee,
        source=result,
        description=description,
        statement_descriptor='Apptitude',
    )

    return [results, fee]


def generate_application_number(user):
    import secrets
    from datetime import date
    low = 100
    high = 5000000
    out = secrets.randbelow(high - low) + low  # out = random number from range [low, high)
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    # return '%s%s%s%s' %(user,d1,productInsuree,out)
    return '%s%s%s' % (user, d1, out)


def generate_claims_refno():
    length = 12
    Numbers = string.digits

    printable = f'{Numbers}'
    printable = list(printable)
    new_ref = random.shuffle(printable)

    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    # print(random_password)
    return random_password


def get_twilio_client():
    client = Client(settings.TWILIO_ACCOUNT_SERVICE_ID, settings.TWILIO_AUTH_TOKEN)
    verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_ID)

    return verify


def get_google_token_info(id_token):
    try:
        google_url = 'https://oauth2.googleapis.com/tokeninfo?id_token=%s' % id_token

        # Get User Data with id_token
        res = requests.get(google_url)

        if (res.status_code == 200):
            return res.json()
    except Exception as e:
        return None


def fbgraph_token_info_vk(access_token):
    try:
        graph = facebook.GraphAPI(access_token=access_token)
        return graph.request('/me?fields=first_name,last_name,email,groups')

    except Exception as e:
        return None
