import logging
import os

from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable
from django.utils.translation import gettext_lazy as _

from digiinsurance.models.Policy import Policy
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.User import User
from digiinsurance.models.Insuree import Insuree

logger = logging.getLogger('blockchain')


class Wallet(models.Model):
    """
    Defines Wallet of User that will contain account details
    and Aptitudes
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet')
    account = models.CharField(max_length=42)
    passphrase = models.CharField(_('password'), max_length=128)
    coins = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return '%s' % self.user

    def create_account(self, passphrase):
        from . import api
        if not self.account:
            try:
                self.account = api.create_account(passphrase)
                self.passphrase = make_password(passphrase)
                if is_password_usable(self.passphrase):
                    logger.info("Account Created for %s - %s" % (
                        self.user, self.account))
                    if api.send_ether(self.account, value=10)[0]:
                        self.save()
                    return self.account
                else:
                    logger.error('Password Not Usable')
                    return None

            except Exception as e:
                logger.error(e)
                return None
        else:
            logger.error(
                "Wallet of %s has existing account already" % self.user)


class Contract(models.Model):
    """
    Defines a Contract in the blockchain
    """

    owner = models.CharField(max_length=42)
    address = models.CharField(max_length=42)
    name = models.CharField(max_length=32, unique=True)
    abi = models.TextField()

    def __str__(self):
        return '%s' % self.name


def upload_certificate(instance, filename):
    name = "{}.{}".format(instance.address, 'jpg')
    return os.path.join('certificates', name)


class CertificateAddress(models.Model):
    """
    Stores hash/address of Certificates of students
    """
    insureePolicy = models.OneToOneField(InsureePolicy, on_delete=models.CASCADE,related_name='certificate_address',
                                         null=True, blank=True)
    address = models.CharField(max_length=42)
    timestamp = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_certificate, null=True, blank=True)

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True, blank=True, related_name='certificates')
    insuree = models.ForeignKey(Insuree, on_delete=models.CASCADE, null=True, blank=True, related_name='certificates')
    available = models.BooleanField(default=True)

    # could be roll number, license no, etc.
    number = models.CharField(max_length=32, null=True, blank=True)

    # def __str__(self):
    #     if self.enrollment:
    #         return '%s %s %s' % (self.enrollment, self.timestamp, self.number)
    #     return '%s %s %s' % (self.course, self.timestamp, self.number)

    # @property
    # def full_name(self):
    #     if self.enrollment:
    #         return self.enrollment.student.full_name
    #     return self.student.full_name

    # @property
    # def course(self):
    #     if self.enrollment:
    #         return self.enrollment.get_course().name
    #     return self.course.name

    # @property
    # def school(self):
    #     if self.enrollment:
    #         return self.enrollment.get_course().school.name
    #     return None

    @property
    def details(self):
        from blockchain.api import get_certificate

        return get_certificate(self.address)


class Transaction(models.Model):
    TOPUP = 'topup'
    PAYOUT = 'payout'
    TRANSFER = 'transfer'

    TRANSACTION_TYPES = (
        (TOPUP, 'Topup'),
        (PAYOUT, 'Payout'),
        (TRANSFER, 'Transfer'))

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    origin = models.ForeignKey(Wallet, related_name='transactions_from', null=True, blank=True,
                               on_delete=models.SET_NULL)
    destination = models.ForeignKey(Wallet, related_name='transactions_to', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    address = models.CharField(max_length=66)
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '[%s] %s - %s (%s)' % (
            self.type, self.origin, self.destination, self.amount)
