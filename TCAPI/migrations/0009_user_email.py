# Generated by Django 3.1.5 on 2022-10-03 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0008_auto_20220421_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=80, null=True, unique=True),
        ),
    ]
