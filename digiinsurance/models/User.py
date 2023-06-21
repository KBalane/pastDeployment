from __future__ import unicode_literals

import logging
import os

from django.contrib.auth.models import AbstractUser, UserManager
from .Company import Company
from django.db import models

from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')


def upload_user_photo(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users', name)


class User(AbstractUser):
    INSUREE = 'IN'
    INSURANCE_COMPANY = 'CO'
    INSURANCE_STAFF = 'ST'
    ADMIN = 'AD'
    UNDERWRITER = 'UW'
    USER_ROLE = (
        (INSUREE, 'Insuree'),
        (INSURANCE_COMPANY, 'Insurance Admin'),
        (INSURANCE_STAFF, 'Insurance Staff'),
        (UNDERWRITER, 'Underwriter'),
        (ADMIN, 'Admin'),

    )
    email = models.EmailField(max_length=128, unique=True)
    role = models.CharField(max_length=2, choices=USER_ROLE)
    photo = models.ImageField(upload_to=upload_user_photo, null=True, blank=True)
    step = models.PositiveSmallIntegerField(default=1)
    info_submitted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # mobile_verified
    country_code = models.CharField(max_length=5, default='+63', null=True, blank=True)
    mobile_number = models.CharField(max_length=16, null=True, blank=True)

    objects = UserManager()

    class Meta:
        app_label = 'digiinsurance'
        permissions = (
            ('update_permissions', 'Can update permissions'),
            ('view_only', 'View only access'),
        )

    def get_full_name(self):
        # names = [self.first_name, self.middle_name, self.last_name]
        names = [self.first_name, self.last_name]
        return ' '.join(filter(None, names))

    # @property
    # def full_name(self):
    #     names = [self.first_name, self.middle_name, self.last_name]
    #     return ' '.join(filter(None, names))

    @property
    def is_insuree(self):
        return self.role == User.INSUREE

    @property
    def is_company(self):
        return self.role == User.INSURANCE_COMPANY

    # @property
    # def is_staff(self):
    #     return self.role == User.INSURANCE_STAFF

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def email_domain(self):
        return self.email.split('@')[1]

    @property
    def user_id(self):
        return self.user_ids.filter().first()

    @property
    def kyc_done(self):
        if self.user_ids.filter(verified=True).exists():
            return True
        return False

    @property
    def registration_completed(self):
        return self.step == 0 and self.info_submitted and self.kyc_done and self.is_verified


class Staff(TimeStampedModel):
    user_id = models.ForeignKey('digiinsurance.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=(('F', 'Female'), ('M', 'Male')))
    email = models.EmailField(max_length=128, blank=True, null=True)
    mobile_number = models.CharField(max_length=16, null=False, blank=False, unique=True)
    insurance_company = models.ManyToManyField(Company, related_name='insurance_staff', blank=True)

    def __str__(self):
        return self.user_id.full_name
