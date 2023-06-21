# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from datetime import date

from django.db import models

from .extras import TimeStampedModel

import os


logger = logging.getLogger('digiinsurance.models')

__all__ = ['Claims']


def pdf_path(instance, filename):
    # return os.path.join(settings.MEDIA_ROOT, 'media.pdf')

    ext = filename.split('.')[-1]
    name = '{}_{}.{}'.format(instance.id, instance.UserPolicy_id, ext)
    return os.path.join('claims', name)


def upload_to_claims(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users', name)


class Claims(TimeStampedModel):
    # UserPolicy_id = models.PositiveSmallIntegerField(blank=True, null=True)
    UserPolicy_id = models.ForeignKey(
        'InsureePolicy', related_name='Insuree', on_delete=models.CASCADE)

    # Adding the status
    CLAIM_STATUS = (
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('pending', 'Pending')
    )

    bank_name = models.CharField(max_length=256, null=True)
    created_at = date.today()
    claim_type = models.CharField(max_length=30, null=True, default="")
    claim_docs = models.FileField(default='timezone.now', upload_to=upload_to_claims, max_length=None)
    claims_refno = models.CharField(max_length=256, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=8)
    claim_status = models.CharField(max_length=10, default='pending', choices=CLAIM_STATUS)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def get_creation_date(self):
        return self.created_at

    @property
    def get_userpolicy_id(self):
        return self.UserPolicy_id

    @property
    def get_id(self):
        return self.id

    """ @property
    def get_claims_refno(self):
        #claims_refno = getclaimsrefno(self)
        return '{}-{}'.format(self.create_at, self.id) """

    def save(self, *args, **kwargs):
        self.claims_refno = str(self.created_at)
        super().save(*args, **kwargs)
