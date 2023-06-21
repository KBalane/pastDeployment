from django.contrib import admin

# Register your models here.
from blockchain.models import *


class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ('passphrase', 'account', 'coins')


class ContractAdmin(admin.ModelAdmin):
    readonly_fields = ('address', 'owner', 'name', 'abi')


class CertificateAddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        'address', 'timestamp', 'number', 'insuree', 'policy')


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'type', 'amount', 'origin', 'destination', 'address', 'timestamp')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(CertificateAddress, CertificateAddressAdmin)
admin.site.register(Transaction, TransactionAdmin)
