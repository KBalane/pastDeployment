from __future__ import unicode_literals

import logging

from digiinsurance.models import Beneficiaries

from django.db import models

from .extras import TimeStampedModel

from .InsureePolicy import InsureePolicy

logger = logging.getLogger('digiinsurance.models')

__all__ = ['TempBeneficiaries']


class TempBeneficiaries(TimeStampedModel):
    # beneficiary = models.ForeignKey(
    # Beneficiaries, related_name='beneficiaries', on_delete=models.CASCADE)
    beneficiary = models.IntegerField()
    birthplace = models.CharField(max_length=32, default="Birthplace", blank=False, null=False)
    country = models.CharField(max_length=32, default="Country", blank=False, null=False)
    birthday = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=32, default="Nationality", blank=False, null=False)
    beneficiary_address = models.CharField(max_length=255, default="Beneficiary address", null=False)
    request = models.CharField(max_length=255, default="N/A", blank=True, null=True)
    reason = models.CharField(max_length=255, default="Reason", null=False)

    user_policy = models.ForeignKey(InsureePolicy, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=32, blank=False, null=False, default="name")
    middle_name = models.CharField(max_length=32, blank=True, null=True, default="name")
    last_name = models.CharField(max_length=32, blank=False, null=False, default="name")
    relationship = models.CharField(max_length=16, blank=False, null=True)
    beneficiary_status = models.CharField(max_length=8, choices=Beneficiaries.STATUS, default="Pending")
    percentage_of_share = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        app_label = 'digiinsurance'
