# Generated by Django 3.1.6 on 2021-08-13 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0013_auto_20210813_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempbeneficiaries',
            old_name='benefeciary_status',
            new_name='beneficiary_status',
        ),
    ]