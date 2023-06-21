# Generated by Django 3.1 on 2021-10-27 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0011_auto_20211027_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolicyOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=64, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=32)),
                ('mobile_number', models.CharField(max_length=16, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=1, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('tel_number', models.CharField(blank=True, max_length=16, null=True)),
                ('occupation', models.CharField(blank=True, max_length=64, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=64, null=True)),
                ('nationality', models.CharField(blank=True, max_length=64, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=128, null=True)),
                ('sss', models.CharField(blank=True, max_length=16, null=True)),
                ('tin', models.CharField(blank=True, max_length=16, null=True)),
                ('business', models.CharField(blank=True, max_length=64, null=True)),
                ('home_address', models.CharField(blank=True, max_length=254, null=True)),
                ('home_village', models.CharField(blank=True, max_length=254, null=True)),
                ('home_city', models.CharField(blank=True, max_length=64, null=True)),
                ('home_province', models.CharField(blank=True, max_length=64, null=True)),
                ('home_zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('nature_of_business', models.CharField(blank=True, max_length=64, null=True)),
                ('specified_source', models.CharField(blank=True, max_length=64, null=True)),
                ('source_of_funds', models.CharField(blank=True, max_length=64, null=True)),
                ('office_address', models.CharField(blank=True, max_length=254, null=True)),
                ('office_province', models.CharField(blank=True, max_length=64, null=True)),
                ('office_zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('office_village', models.CharField(blank=True, max_length=64, null=True)),
                ('office_city', models.CharField(blank=True, max_length=64, null=True)),
                ('insured_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocolife.DigiInsuree')),
                ('product_insuree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocolife.ProductInsuree')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
