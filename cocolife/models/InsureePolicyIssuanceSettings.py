from django.db import models
from digiinsurance.models.extras import TimeStampedModel

__all__ = ['InsureePolicyIssuanceSettings']


class InsureePolicyIssuanceSettings(TimeStampedModel):
    policy = models.BooleanField(default=True)
    insuree = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    premium_amount_due = models.BooleanField(default=True)
    premium_date_due = models.BooleanField(default=True)
    premium_last_paid = models.BooleanField(default=True)
    premium_last_date = models.BooleanField(default=True)
    policy_type = models.BooleanField(default=True)
    policy_type2 = models.BooleanField(default=True)
    active_premium_interval = models.BooleanField(default=True)
    Currency = models.BooleanField(default=True)
