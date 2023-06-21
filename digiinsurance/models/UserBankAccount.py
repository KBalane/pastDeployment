from __future__ import unicode_literals

import logging

from datetime import date, datetime

from django.db import models

from digiinsurance.models.User import User
from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')


class UserBankAccount(TimeStampedModel):
    user = models.ForeignKey(User, related_name='userbankaccount', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_branch = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    is_preferred = models.BooleanField(default=False)
