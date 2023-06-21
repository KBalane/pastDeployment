import logging
import os
from decimal import Decimal
from django.db import models
from digiinsurance.models import Company, User, Insuree, InsureePolicy

logger = logging.getLogger('digiinsurance.models')

__all__ = ['CompanyInvestmentType', 'UserInvestment']


def facts_sheet(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('company', name)


def upload_investment_image(instance, filename):
    name = "{}.{}".format(instance.id, 'jpg')
    return os.path.join('company', name)


class CompanyInvestmentType(models.Model):
    company = models.ForeignKey(Company, related_name='Investment', on_delete=models.CASCADE, null=True, blank=True)
    risk_rate = models.FloatField()
    investment_name = models.CharField(max_length=255, blank=True, null=True)
    invest_description = models.CharField(max_length=255, blank=True, null=True)
    investment_term = models.CharField(max_length=255, blank=True, null=True)
    income_bracket = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    risk_tolerance = models.CharField(max_length=255, blank=True, null=True)
    other_information = models.TextField()
    product_image = models.ImageField(upload_to=upload_investment_image, null=True, blank=True)
    facts_sheet = models.FileField(upload_to=facts_sheet, blank=True, null=True)

    def __str__(self):
        return '[%s] %s-%s' % (self.id, self.investment_name, self.company)


class UserInvestment(models.Model):
    PAID = 'paid'
    NOTPAID = 'notpaid'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    EXPIRED = 'expired'

    INVESTMENT_INTERVALS = (
        ('annual', 'Annual'),
        ('one_time', 'One Time'),
        ('semi_annual', 'Semi Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly')
    )

    STATUS_CHOICES = (
        (PAID, 'Paid'),
        (NOTPAID, 'Not Paid'),
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (EXPIRED, 'Expired'),
    )

    userpolicy_Id = models.ForeignKey(InsureePolicy, related_name='user_investor', on_delete=models.CASCADE)
    investor_id = models.ForeignKey(Insuree, null=True, blank=True, related_name='investor_id', on_delete=models.CASCADE)
    investment_type = models.ForeignKey(CompanyInvestmentType, null=True, blank=True, on_delete=models.CASCADE)
    available_investment_interval = models.CharField(max_length=64, default='Annual', choices=INVESTMENT_INTERVALS)
    initial_dep = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    succ_dep_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    number_of_yearspayment = models.IntegerField()
    partial_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    future_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    investment_status = models.CharField(max_length=10, default='Active', choices=STATUS_CHOICES)
    investment_refno = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '[%s] %s-%s, %s' % (self.id, self.investor_id, self.investment_type, self.investment_status)
