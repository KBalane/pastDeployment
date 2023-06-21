# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models

from digiinsurance.models.extras import TimeStampedModel, ArchivedModel, CompletableModel

from .DigiInsuree import DigiInsuree
from .ProductInsuree import ProductInsuree

from django.utils import timezone

__all__ = ['DigiTransaction']


class DigiTransaction(TimeStampedModel, ArchivedModel, CompletableModel):
    FULL_PAYMENT = 'full'
    LOAN_PAYMENT = 'loan'

    BANK_ONLINE = 'online_bank'
    BANK_OTC = 'otc_bank'
    OTHERS = 'others'
    CASH = 'cash'
    CARD = 'card'

    MAGPIE = 'magpie'
    DRAGONPAY = 'dp'
    VOUCHER = 'voucher'

    PAYMENT_TYPES = (
        (FULL_PAYMENT, 'Full Payment'),
        (LOAN_PAYMENT, 'Loan Payment')
    )

    PROCESSOR_TYPES = (
        (BANK_ONLINE, 'Online/Mobile Bank'),
        (BANK_OTC, 'Bank Over the Counter'),
        (OTHERS, 'Others'),
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (VOUCHER, 'Voucher')
    )
    PAYMENT_CHANNELS = (
        (MAGPIE, 'Magpie'),
        (DRAGONPAY, 'Dragonpay'),
        (CASH, 'Cash'),
        (VOUCHER, 'Voucher')
    )

    PROCESSORS = (
        ('BOGX', 'Bogus Bank Over-the-Counter'),
        ('BDOA', 'Banco de Oro ATM'),
        ('BDRX', 'BDO Cash Deposit'),
        ('BPXB', 'BPI Bills Payment'),
        ('BNRX', 'BDO Network Bank (formerly ONB) Cash Dep'),
        ('AUB', 'AUB Online/Cash Payment'),
        ('MBTX', 'Metrobank Cash/Check Payment'),
        ('CBCX', 'Chinabank ATM/Cash Payment'),
        ('EWXB', 'EastWest Online/Cash Payment'),
        ('I2I', 'i2i Rural Banks'),
        ('LBXB', 'Landbank Cash Payment'),
        ('PNBB', 'PNB e-Banking Bills Payment'),
        ('PNXB', 'PNB Cash Payment'),
        ('RCXB', 'RCBC Cash Payment'),
        ('RSXB', 'RCBC Savings Cash Payment'),
        ('SBCA', 'Security Bank ATM Bills Payment'),
        ('SBCB', 'Security Bank Cash Payment'),
        ('RSBB', 'RobinsonsBank Cash Payment'),
        ('UBXB', 'Unionbank Cash Payment'),
        ('UCXB', 'UCPB ATM/Cash Payment'),
        ('BOG', 'Bogus Bank'),
        ('BDO', 'BDO Internet Banking'),
        ('BPIA', 'BPI Online/Mobile (NEW)'),
        ('BPI', 'BPI Express Online (Fund Transfer)'),
        ('BPIB', 'BPI Express Online (Bills Payment)'),
        ('MBTC', 'Metrobank Direct Online'),
        ('CBC', 'Chinabank Online'),
        ('LBPA', 'Landbank iAccess'),
        ('MAYB', 'Maybank Online Banking'),
        ('PSB', 'PSBank Online'),
        ('RCBC', 'RCBC Online Banking'),
        ('UBP', 'UnionBank eBanking'),
        ('UBPB', 'Unionbank Internet Banking'),
        ('UCPB', 'UCPB Connect'),
        ('BITC', 'Coins.ph Wallet / Bitcoin'),
        ('GRPY', 'GrabPay'),
        ('BAYD', 'Bayad Center'),
        ('LBC', 'LBC'),
        ('SMR', 'SM Dept/Supermarket/Savemore Counter'),
        ('CEBL', 'Cebuana Lhuillier Bills Payment'),
        ('PLWN', 'Palawan Pawnshop'),
        ('MLH', 'M. Lhuillier'),
        ('RDP', 'RD Pawnshop'),
        ('RDS', 'Robinsons Dept Store'),
        ('ECPY', 'ECPay (Pawnshops, Payment Centers)'),
        ('RLNT', 'RuralNet Banks and Coops'),
        ('CASH', 'Cash Payment'),
        ('VISA', 'Visa'),
        ('MC', 'Mastercard'),
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('VOUCHER', 'Voucher')
    )
    # fields:
    # payment method = enum/dipwdown
    # client/customer = foreign key
    # sentHardCopy = boolean
    # interval = monthly, annual, semi annual
    # total = example: (Total: PHP 100.00 per month) call productinsuree

    cocoinsuree = models.ForeignKey(DigiInsuree, related_name='transactions', on_delete=models.CASCADE)
    # payment method:
    channel = models.CharField(max_length=32, choices=PAYMENT_CHANNELS, null=True, blank=True)
    payment_type = models.CharField(max_length=6, choices=PAYMENT_TYPES, default=FULL_PAYMENT)
    processor_type = models.CharField(max_length=16, choices=PROCESSOR_TYPES, null=True, blank=True)
    processor = models.CharField(max_length=10, choices=PROCESSORS, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    productinsuree = models.ForeignKey(ProductInsuree, related_name='cl_transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    txn_id = models.CharField(max_length=64, null=True, blank=True)
    # updated_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'cocolife'

    def __str__(self):
        return '[%s] %s %s' % (self.processor_type, self.productinsuree,
                               self.completed_at)

    def send_payment_confirmation_email(self, ref_num, productInsuree_id, to_email):
        return send_mail(
            'Payment Confirmation',  # title
            '''
            Thank you for your payment!

            Transaction Number: %s
            Policy Number: %s''' % (ref_num, productInsuree_id),  # body
            'marketing@qymera.tech',  # from
            ['%s' % (to_email)],  # to (recepient)
            fail_silently=False)

    def complete(self):
        # from api.tasks.email import send_payment_receipt_email

        # if self.completed_at:
        #     logger.debug('%r already completed', self)
        #     return False

        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])
        self.send_payment_confirmation_email(
            self.txn_id, self.productinsuree, self.cocoinsuree.user.email)

        # TODO If there are any other actions to be done after
        # a successful payout, place it here

        return True

# if true hardcopy{

#     customer: van keith
#     policy file pdf: hvckyvb/jhvkuybl/xxlhv.pdf 
#     custyomer address: 13 libliubl phillipines
#     #isDelivered: yes/no

# }
