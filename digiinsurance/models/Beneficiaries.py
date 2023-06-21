from __future__ import unicode_literals

import logging

from datetime import date, datetime

from django.db import models

from .extras import TimeStampedModel
from .InsureePolicy import InsureePolicy

logger = logging.getLogger('digiinsurance.models')

__all__ = ['Beneficiaries']


def default_json_list():
    return {'no_values': []}


class Beneficiaries(TimeStampedModel):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DENIED = 'DENIED'
    ADD = 'ADD'
    UPDATE = 'UPDATE'
    REMOVE = 'REMOVE'
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'APPROVED'),
        (DENIED, 'Denied'),
    )

    REQUESTTYPE = (
        (ADD, 'Add'),
        (UPDATE, 'Update'),
        (REMOVE, 'Remove'),
    )
    user_policy = models.ForeignKey(InsureePolicy, related_name='user_policy', on_delete=models.CASCADE)
    # models.PositiveSmallIntegerField(blank=False, null=False)
    first_name = models.CharField(max_length=32, blank=False, null=False)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=False, null=False)
    relationship = models.CharField(max_length=16, blank=False, null=True)
    birthday = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=32, default="Birthplace", blank=False, null=False)
    nationality = models.CharField(max_length=32, default="Nationality", blank=False, null=False)
    country = models.CharField(max_length=32, default="Country", blank=False, null=False)
    beneficiary_address = models.CharField(max_length=255, default="Beneficiary address", null=False)
    beneficiary_status = models.CharField(max_length=8, choices=STATUS, default="Pending")
    request_type = models.CharField(max_length=8, choices=REQUESTTYPE, default="Add")
    percentage_of_share = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    reason = models.CharField(max_length=255, default="Reason", null=False)
    update_fields = models.JSONField(null=True, blank=True, default=default_json_list)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def get_user_policy_id(self):
        return self.user_policy_id

    @property
    def full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, names))

    def age(self):
        today = date.today()
        born = self.birthday

        try:
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(
                year=today.year, month=born.month + 1, day=1)
        except:
            return

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    @property
    def get_relationship(self):
        return self.relationship

