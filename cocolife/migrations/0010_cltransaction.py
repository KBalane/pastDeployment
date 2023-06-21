# Generated by Django 3.1 on 2021-10-25 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0009_auto_20211020_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('archived_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('txn_id', models.CharField(blank=True, max_length=64, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('channel', models.CharField(blank=True, choices=[('magpie', 'Magpie'), ('dp', 'Dragonpay'), ('cash', 'Cash'), ('voucher', 'Voucher')], max_length=32, null=True)),
                ('payment_type', models.CharField(choices=[('full', 'Full Payment'), ('loan', 'Loan Payment')], default='full', max_length=6)),
                ('processor_type', models.CharField(blank=True, choices=[('online_bank', 'Online/Mobile Bank'), ('otc_bank', 'Bank Over the Counter'), ('others', 'Others'), ('cash', 'Cash'), ('card', 'Card'), ('voucher', 'Voucher')], max_length=16, null=True)),
                ('processor', models.CharField(blank=True, choices=[('BOGX', 'Bogus Bank Over-the-Counter'), ('BDOA', 'Banco de Oro ATM'), ('BDRX', 'BDO Cash Deposit'), ('BPXB', 'BPI Bills Payment'), ('BNRX', 'BDO Network Bank (formerly ONB) Cash Dep'), ('AUB', 'AUB Online/Cash Payment'), ('MBTX', 'Metrobank Cash/Check Payment'), ('CBCX', 'Chinabank ATM/Cash Payment'), ('EWXB', 'EastWest Online/Cash Payment'), ('I2I', 'i2i Rural Banks'), ('LBXB', 'Landbank Cash Payment'), ('PNBB', 'PNB e-Banking Bills Payment'), ('PNXB', 'PNB Cash Payment'), ('RCXB', 'RCBC Cash Payment'), ('RSXB', 'RCBC Savings Cash Payment'), ('SBCA', 'Security Bank ATM Bills Payment'), ('SBCB', 'Security Bank Cash Payment'), ('RSBB', 'RobinsonsBank Cash Payment'), ('UBXB', 'Unionbank Cash Payment'), ('UCXB', 'UCPB ATM/Cash Payment'), ('BOG', 'Bogus Bank'), ('BDO', 'BDO Internet Banking'), ('BPIA', 'BPI Online/Mobile (NEW)'), ('BPI', 'BPI Express Online (Fund Transfer)'), ('BPIB', 'BPI Express Online (Bills Payment)'), ('MBTC', 'Metrobank Direct Online'), ('CBC', 'Chinabank Online'), ('LBPA', 'Landbank iAccess'), ('MAYB', 'Maybank Online Banking'), ('PSB', 'PSBank Online'), ('RCBC', 'RCBC Online Banking'), ('UBP', 'UnionBank eBanking'), ('UBPB', 'Unionbank Internet Banking'), ('UCPB', 'UCPB Connect'), ('BITC', 'Coins.ph Wallet / Bitcoin'), ('GRPY', 'GrabPay'), ('BAYD', 'Bayad Center'), ('LBC', 'LBC'), ('SMR', 'SM Dept/Supermarket/Savemore Counter'), ('CEBL', 'Cebuana Lhuillier Bills Payment'), ('PLWN', 'Palawan Pawnshop'), ('MLH', 'M. Lhuillier'), ('RDP', 'RD Pawnshop'), ('RDS', 'Robinsons Dept Store'), ('ECPY', 'ECPay (Pawnshops, Payment Centers)'), ('RLNT', 'RuralNet Banks and Coops'), ('CASH', 'Cash Payment'), ('VISA', 'Visa'), ('MC', 'Mastercard'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('VOUCHER', 'Voucher')], max_length=10, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('cocoinsuree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='cocolife.DigiInsuree')),
                ('productinsuree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='cocolife.ProductInsuree')),
            ],
        ),
    ]
