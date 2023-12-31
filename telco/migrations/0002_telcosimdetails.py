# Generated by Django 3.1 on 2022-10-21 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelcoSimDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('number_owner', models.CharField(blank=True, max_length=16, null=True)),
                ('owner_relationship', models.CharField(blank=True, max_length=30, null=True)),
                ('minor_name', models.CharField(blank=True, max_length=50, null=True)),
                ('purpose', models.CharField(blank=True, max_length=50, null=True)),
                ('sim_card_serial', models.CharField(blank=True, max_length=50, null=True)),
                ('sim_card_number', models.CharField(blank=True, max_length=50, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personsim', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
