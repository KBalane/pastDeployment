# Generated by Django 3.1 on 2021-09-14 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0017_auto_20210825_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='is_recommended',
            field=models.BooleanField(default=False),
        ),
    ]
