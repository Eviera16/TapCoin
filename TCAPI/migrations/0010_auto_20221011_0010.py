# Generated by Django 3.1.5 on 2022-10-11 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0009_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(max_length=11, null=True, unique=True),
        ),
    ]
