# Generated by Django 3.1 on 2021-10-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0010_auto_20211026_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='age',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='current_add',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='current_country',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='current_zip_code',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='home_add',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='home_country',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='nature_of_business_of_employer',
        ),
        migrations.RemoveField(
            model_name='DigiInsuree',
            name='type',
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='home_address',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='home_city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='home_province',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='home_village',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='nature_of_business',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='office_address',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='office_city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='office_province',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='office_village',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='office_zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='source_of_funds',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='DigiInsuree',
            name='specified_source',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='ProductInsuree',
            name='is_self_insured',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='business',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='home_zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='mobile_number',
            field=models.CharField(default='1', max_length=16, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='nationality',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='occupation',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='DigiInsuree',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.DeleteModel(
            name='PolicyOwner',
        ),
    ]
