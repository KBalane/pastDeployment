# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from digiinsurance.models import Company, Policy

import logging

from datetime import date, datetime

from django.db import models

from .extras import TimeStampedModel
logger = logging.getLogger('digiinsurance.models')
import jsonfield

__all__ = ['CompanyFAQ']


class CompanyFAQ(TimeStampedModel):

    answer = models.CharField(null=True, blank=True, max_length=256)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    question = models.CharField(max_length=256, null=True)
    
    class Meta:
        app_label = 'digiinsurance'
