# Generated by Django 3.1.5 on 2022-10-16 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0015_user_p_code_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_phone_number',
            field=models.BooleanField(default=False, verbose_name='has a phone number'),
        ),
    ]
