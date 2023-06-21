# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from datetime import date, datetime

from django.db import models
from digiinsurance.models.extras import TimeStampedModel
from .Product import Package, Product, Variant
from .DigiInsuree import DigiInsuree
from dateutil.relativedelta import relativedelta

__all__ = ['ProductInsuree']


class ProductInsuree(TimeStampedModel):
    PREMIUM_INTERVALS = (
        ('annual', 'Annual'),
        ('semi_annual', 'Semi Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly')
    )

    STATUS = (
        ('active', 'Active'),  # upon creation - inactive
        ('inactive', 'Inactive'),  # upon payment - active
        ('pending', 'Pending'),  # for underwriting - pending
        ('lapsed', 'Lapsed'),
        ('ended', 'Ended')
    )
    billed_to = models.ForeignKey(DigiInsuree, related_name='productinsurees', on_delete=models.CASCADE)  # USER
    product = models.ForeignKey(Product, related_name='productinsurees', on_delete=models.CASCADE)  # 3
    package = models.ForeignKey(Package, related_name='productinsurees', on_delete=models.CASCADE)  # id = 53
    variant = models.ForeignKey(Variant, related_name='productinsurees', on_delete=models.CASCADE)  # id = 101
    coverage_term = models.IntegerField(null=True, blank=True)  # data is only 1 to 12 only         # id = 5
    payment_term = models.CharField(
        max_length=30, default='monthly', choices=PREMIUM_INTERVALS)
    status = models.CharField(
        max_length=10, default='inactive', choices=STATUS)
    premium_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    premium_due_date = models.DateField(blank=True, null=True)
    premium_last_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    premium_last_date = models.DateField(blank=True, null=True)
    is_self_insured = models.BooleanField(default=True)

    class Meta:
        app_label = 'cocolife'

    def __str__(self):
        return '[%s] %s-%s-%s' % (self.id, self.billed_to, self.product,
                                  self.status)

    def update_due_date(self):
        term_val = {
            'monthly': 1,
            'quarterly': 3,
            'semi annual': 6,
            'annual': 12
        }
        date_to_add = relativedelta(months=+term_val[self.payment_term])
        if self.premium_due_date is None:
            self.premium_due_date = date.today() + date_to_add  # create initial due date
        else:
            self.premium_due_date += date_to_add  # add date to existing value
        self.save(update_fields=['premium_due_date'])

    def get_expiration_date(self):
        date_to_add = relativedelta(years=+self.coverage_term)
        return self.created_at + date_to_add
