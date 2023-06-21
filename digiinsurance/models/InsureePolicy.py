from __future__ import unicode_literals

import logging

from datetime import date, datetime

from django.db import models

from .extras import TimeStampedModel
# from digiinsurance.models import Insuree, Policy
from .Insuree import Insuree
from .Policy import Policy
logger = logging.getLogger('digiinsurance.models')


class InsureePolicy(TimeStampedModel):
    PAID = 'paid'
    NOTPAID = 'notpaid'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    EXPIRED = 'expired'

    STATUS_CHOICES = (
        (PAID, 'Paid'),
        (NOTPAID, 'Not Paid'),
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (EXPIRED, 'Expired'),
    )

    POLICY_CHOICES = (
        ('life', 'Life'),
        ('health', 'Health'),
        ('home', 'Home'),
        ('car', 'Car'),
        ('vul', 'VUL'),
    )

    POLICY_CHOICES2 = (
        ('lite', 'Lite'),
        ('pro', 'Pro'),
        ('standard', 'Standard'),
        ('basic', 'Basic')
    )

    PREMIUM_INTERVALS = (
        ('one_time', 'One Time'),
        ('annual', 'Annual'),
        ('semi_annual', 'Semi Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly')
    )
    policy = models.ForeignKey(Policy, related_name='insuree_policies', on_delete=models.CASCADE)
    insuree = models.ForeignKey(Insuree, related_name='insuree', on_delete=models.CASCADE)

    # is policy insured by self boolean default
    status = models.CharField(max_length=10, default='Active', choices=STATUS_CHOICES)
    premium_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    premium_date_due = models.DateField(blank=True, null=True)
    premium_last_paid = models.DecimalField(max_digits=10, decimal_places=2)
    premium_last_date = models.DateField(blank=True, null=True)
    policy_type = models.CharField(max_length=10, default='Life', choices=POLICY_CHOICES)
    policy_type2 = models.CharField(max_length=10, default='Lite', choices=POLICY_CHOICES2)
    active_premium_interval = models.CharField(max_length=11, default='One time', choices=PREMIUM_INTERVALS)
    Currency = models.CharField(max_length=3, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(InsureePolicy, self).save(*args, **kwargs)
        self.checkStatusPolicy()

    def delete(self, *args, **kwargs):
        super(InsureePolicy, self).delete(*args, **kwargs)
        self.checkStatusPolicy()

    def checkStatusPolicy(self):
        try:
            # RAW QUERY
            # Get those policy ids missing on insureepolicies table + (UNION) + get those ids that are marked "paid"
            inactive_policies = Policy.objects.raw(
                '''SELECT DISTINCT `digiinsurance_policy`.`id` FROM `digiinsurance_policy`  INNER JOIN `digiinsurance_insureepolicy` ON (`digiinsurance_insureepolicy`.`policy_id` = `digiinsurance_policy`.`id`)  WHERE `digiinsurance_insureepolicy`.`status` != 'Active' UNION SELECT `digiinsurance_policy`.`id` FROM `digiinsurance_policy` WHERE `digiinsurance_policy`.`id` NOT IN (SELECT `digiinsurance_insureepolicy`.`policy_id` FROM `digiinsurance_insureepolicy`)''')
            for policy in list(inactive_policies):
                Policy.objects.filter(id=policy.id).update(status="Inactive")
            active_policies = InsureePolicy.objects.all().values_list('policy').filter(status='Active').distinct()
            for id in list(active_policies):
                Policy.objects.filter(id=id[0]).update(status="active")
        except Exception as e:
            logger.exception(e)

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return '[%s] %s-%s-%s' % (self.id, self.insuree, self.policy, self.status)
