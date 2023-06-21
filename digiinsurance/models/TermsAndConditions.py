# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

from django.db import models


from .extras import TimeStampedModel
from digiinsurance.models.Company import Company

logger = logging.getLogger('digiinsurance.models')

__all__ = ['TermsAndCondition']


def pdf_path(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('terms/', name)


def default_json_list():
    return {'no_values': []}


class TermsAndCondition(TimeStampedModel):
    company = models.ForeignKey(Company, related_name='terms_and_conditions', on_delete=models.CASCADE, blank=True,
                                null=True)
    pdfUpload = models.FileField(upload_to=pdf_path, max_length=None, blank=True, null=True)
