# Generated by Django 3.1.5 on 2022-10-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0016_user_has_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='streak_time',
            field=models.DateTimeField(null=True, verbose_name='win streak time'),
        ),
    ]
