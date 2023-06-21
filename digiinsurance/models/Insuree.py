from __future__ import unicode_literals

import logging
import os
from datetime import date, datetime, timedelta

from django.conf import settings
from django.db import models

from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')


class Insuree(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='Insuree', null=False, on_delete=models.CASCADE,
                                primary_key=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=False)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=(('F', 'Female'), ('M', 'Male')))
    email = models.EmailField(max_length=128, unique=True)
    mobile_number = models.CharField(max_length=16, null=True, blank=False, unique=True)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    current_add = models.CharField(max_length=555, blank=True, null=True)
    occupation = models.CharField(max_length=555, blank=True, null=True)

    civil_status = models.CharField(max_length=64, blank=True, null=True)
    nationality = models.CharField(max_length=16, blank=True, null=True)
    place_of_birth = models.CharField(max_length=64, blank=True, null=True)
    sss = models.CharField(max_length=16, blank=True, null=True)
    tin = models.CharField(max_length=16, blank=True, null=True)
    business = models.CharField(max_length=16, blank=True, null=True)

    tel_number = models.CharField(max_length=16, blank=True, null=True)
    home_add = models.CharField(max_length=555, blank=True, null=True)
    home_country = models.CharField(max_length=16, blank=True, null=True)
    home_zip_code = models.CharField(max_length=4, blank=True, null=True)
    current_country = models.CharField(max_length=16, blank=True, null=True)
    current_zip_code = models.CharField(max_length=4, blank=True, null=True)
    employer = models.CharField(max_length=16, blank=True, null=True)
    nature_of_business_of_employer = models.CharField(max_length=16, blank=True, null=True)
    isArchived = models.BooleanField(default=False)
    type = models.CharField(max_length=1, blank=True, null=True, default='N', choices=(
        ('N', 'New'), ('E', 'Existing'), ('O', 'Others')))

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        # return '[%s] %s' % (self.id, self.full_name)
        return '%s' % self.full_name

    def save(self, *args, **kwargs):
        self.age = self.get_age()
        super(Insuree, self).save(*args, **kwargs)

    def get_age(self):
        """Calculates the age of the user."""
        today = date.today()
        born = self.birthday

        try:
            birthday = born.replace(year=today.year)
        # raised when birth date is February 29 and the current year is not a
        # leap year
        except ValueError:
            birthday = born.replace(
                year=today.year, month=born.month + 1, day=1)
        except:  # generic error
            return

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    @property
    def full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, names))

    @property
    def full_name_lastname(self):
        return '%s, %s %s' % (
            self.last_name, self.first_name, self.middle_name)


class InsureePaymentDetails(TimeStampedModel):
    insuree_id = models.ForeignKey(Insuree, related_name='insuree_payment_details', null=True, on_delete=models.CASCADE)
    app_label = 'digiinsurance'
    accountNumber = models.CharField(max_length=64, blank=True, null=True)
