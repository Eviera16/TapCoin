# Generated by Django 3.1.5 on 2022-10-13 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0013_auto_20221012_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_guest',
            field=models.BooleanField(default=False, verbose_name='is guest'),
        ),
    ]
