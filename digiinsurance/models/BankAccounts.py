from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models


from .extras import TimeStampedModel


class BankAccount(TimeStampedModel):
    """Records of financial accounts of Users."""
    BANK_PROVIDERS = (
        ('AUB', 'Asia United Bank'),
        ('BDO', 'Banco De Oro'),
        ('BPI', 'Bank of the Philippine Islands'),
        ('CBC', 'Chinabank'),
        ('EWB', 'Eastwest Bank'),
        ('LBP', 'Land Bank of the Philippines'),
        ('MBTC', 'Metrobank'),
        ('PNB', 'Philippine National Bank'),
        ('RCBC', 'Rizal Commercial Banking Corporation'),
        ('SBC', 'Security Bank'),
        ('UBP', 'Union Bank'),
        ('UCPB', 'United Coconut Planters Bank'),
        # ('PSB', 'PS Bank'),
    )

    numeric = RegexValidator(r'^[0-9]*$', 'Account number should be numeric')

    company = models.OneToOneField(
        'company', related_name='bank_account', on_delete=models.CASCADE)
    provider = models.CharField(max_length=255, choices=BANK_PROVIDERS)
    branch = models.CharField(max_length=128, default='NA')
    account_name = models.CharField(max_length=128)
    account_number = models.CharField(
        max_length=32, unique=True, validators=[numeric])

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return '[%s] %s: %s' % (
            self.company.name, self.provider, self.account_number)

    @property
    def account_number_masked(self):
        return "%s%s" % (
            "*" * (len(self.account_number) - 4),
            self.account_number[-4:])
