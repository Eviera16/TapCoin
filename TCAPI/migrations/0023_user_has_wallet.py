# Generated by Django 3.1.5 on 2023-12-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0022_auto_20231128_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_wallet',
            field=models.BooleanField(default=False, verbose_name='has wallet'),
        ),
    ]
