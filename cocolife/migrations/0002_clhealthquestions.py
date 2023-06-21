# Generated by Django 3.1 on 2021-10-19 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocolife', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLHealthQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('choices', models.JSONField(blank=True, null=True)),
                ('correct_answer', models.CharField(blank=True, max_length=256, null=True)),
                ('question', models.CharField(max_length=256, null=True)),
                ('question_type', models.CharField(choices=[('MultilineText', 'multiline_text'), ('Number', 'number'), ('MultipleChoice', 'multiple_choice'), ('Yes/No', 'yes/no')], default='MultilineText', max_length=20)),
                ('prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocolife.product')),
            ],
        ),
    ]