# Generated by Django 3.1 on 2021-10-20 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0002_auto_20211020_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to=models.CharField(blank=True, default='pdf', max_length=255, null=True)),
        ),
        migrations.AddField(
            model_name='product',
            name='pdfname',
            field=models.CharField(blank=True, default='pdf', max_length=255, null=True),
        ),
    ]
