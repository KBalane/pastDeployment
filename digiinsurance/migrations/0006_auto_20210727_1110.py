# Generated by Django 3.1 on 2021-07-27 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digiinsurance', '0005_auto_20210723_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='insuree',
            old_name='sss_tin',
            new_name='sss',
        ),
        migrations.AddField(
            model_name='insuree',
            name='tin',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]