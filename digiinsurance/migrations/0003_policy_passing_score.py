# Generated by Django 3.1 on 2021-07-19 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0002_auto_20210715_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='passing_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]