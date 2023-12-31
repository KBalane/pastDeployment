# Generated by Django 3.1 on 2021-10-26 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0009_auto_20211020_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productinsuree',
            old_name='payment_terms',
            new_name='payment_term',
        ),
        migrations.AlterField(
            model_name='productinsuree',
            name='premium_last_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='productinsuree',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
    ]
