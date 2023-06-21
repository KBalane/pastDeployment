from __future__ import unicode_literals

import logging
import os
from django.db import models

from .extras import TimeStampedModel

# from digiinsurance.models import User, Company
from .User import User
from .Company import Company

logger = logging.getLogger('digiinsurance.models')

__all__ = ['Policy', 'PolicyCalculator', 'PolicyRequirements']


def upload_policy_icon(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users', name)


def pdf_path(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users', name)


def default_json_list():
    return {'no_values': []}


class Policy(TimeStampedModel):
    # COURSE_CATEGORIES = (
    #     ('educ', 'Education'),
    #     ('retirement', 'Retirement'),
    #     ('health', 'Health'),
    #     ('group', 'Group'),
    #     ('il', 'Investment Linked')
    # )

    POLICY_CHOICES = (
        ('life', 'Life'),
        ('health', 'Health'),
        ('home', 'Home'),
        ('car', 'Car'),
        ('vul', 'VUL'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('draft', 'Draft'),
    )

    PREMIUM_INTERVALS = (
        ('one_time', 'One Time'),
        ('annual', 'Annual'),
        ('semi_annual', 'Semi Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly')
    )

    FULL_PAYMENT = 'full'
    LOAN_PAYMENT = 'loan'

    PAYMENT_TYPES = (
        (FULL_PAYMENT, 'Full Payment'),
        (LOAN_PAYMENT, 'Loan Payment')
    )

    company = models.ForeignKey(Company, related_name='Policies', on_delete=models.CASCADE, null=True, blank=True, default=1)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # benefits = models.JSONField(null=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=64, blank=True, null=True, choices=POLICY_CHOICES)
    question = models.ForeignKey('HealthQuestions', on_delete=models.CASCADE,max_length=256, blank=True, null=True, default="")
    # premium_details = models.CharField(max_length=255, blank=True, null=True)
    # payment_type = models.ManyToManyField('Transaction', max_length=6,choices=PAYMENT_TYPES, default=FULL_PAYMENT)
    # policy_details = models.CharField(max_length=255, blank=True, null=True)
    # available_premium_interval = models.CharField(
    # max_length=64, blank=True, null=True, choices=PREMIUM_INTERVALS)
    icon_name = models.CharField(max_length=32, blank=True, null=True)
    icon_file = models.FileField(upload_to=upload_policy_icon, blank=True, null=True)
    primary_color = models.CharField(max_length=32, blank=True, null=True)
    is_recommended = models.BooleanField(default=False, null=False)
    # file=models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'media'))
    adminupload=models.FileField(upload_to=pdf_path,max_length=None, blank = True, null=True)
    pdfname=models.CharField(max_length=255, default = 'pdf',blank=True, null=True)
    ADD = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Premium_ADD = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank = True, null=True)
    Premium_TPD = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank = True, null=True)
    Premium_WPTPD=models.CharField(max_length=100, blank=True, null=True)
    TPD = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    WPTPD=models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True, choices=STATUS_CHOICES)
    payment_option = models.JSONField(null=True, blank=True, default=default_json_list)
    packages = models.JSONField(null=True, blank=True, default=default_json_list)
    payment_interval = models.JSONField(null=True, blank=True, default=default_json_list)
    passing_score = models.IntegerField(null=True, blank=True)
    benefits_basic=models.FileField(upload_to=pdf_path,max_length=None, blank = True, null=True)
    benefits_lite=models.FileField(upload_to=pdf_path,max_length=None, blank = True, null=True)
    benefits_standard=models.FileField(upload_to=pdf_path,max_length=None, blank = True, null=True)
    benefits_pro=models.FileField(upload_to=pdf_path,max_length=None, blank = True, null=True)
    """
    ADD decimal(10,2) 
    Premium_ADD decimal(10,2) 
    Premium_TPD decimal(10,2) 
    Premium_WPTPD varchar(100) 
    TPD decimal(10,2) 
    WPTPD varchar(100)
    """

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return '[%s] %s-%s' % (self.id, self.company, self.name)


class PolicyCalculator(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, blank=True, null=True)
    policy_length = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_sum_assured = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    yesorno = models.BooleanField(default=False)


class PolicyRequirements(models.Model):
    policy = models.ForeignKey(
        'Policy', related_name='requirements', on_delete=models.CASCADE,
        null=True, blank=True)
    policy_requirements = models.CharField(max_length= 64, null=True, blank=True)
    policy_req_def = models.TextField(null=True, blank=True)
