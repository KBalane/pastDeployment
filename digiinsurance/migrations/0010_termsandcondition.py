# Generated by Django 3.1 on 2021-08-10 08:07

import digiinsurance.models.TermsAndConditions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0009_auto_20210805_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('pdfUpload', models.FileField(blank=True, null=True, upload_to=digiinsurance.models.TermsAndConditions.pdf_path)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
