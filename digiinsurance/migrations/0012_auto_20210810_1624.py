# Generated by Django 3.1.6 on 2021-08-10 08:24

import digiinsurance.models.Beneficiaries
from django.db import migrations, models
from digiinsurance.models.Beneficiaries import default_json_list


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0011_beneficiaries_update_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Beneficiaries',
            name='update_fields',
            field=models.JSONField(blank=True, default=default_json_list, null=True),
        ),
    ]
