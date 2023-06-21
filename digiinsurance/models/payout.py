# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from datetime import date, datetime 

from django.db import models

from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')

__all__ = ['Payout']


class Payout(TimeStampedModel):
    insurance_company_id = models.PositiveSmallIntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    claim_id = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def get_insurance_company_id(self):
        return self.insurance_company_id

    @property
    def get_amount(self):
        return self.amount

    @property
    def get_claim_id(self):
        return self.claim_id
