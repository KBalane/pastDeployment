# Generated by Django 3.1.6 on 2021-08-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0010_beneficiaries_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiaries',
            name='update_fields',
            field=models.JSONField(blank=True, default='', null=True),
        ),
    ]
