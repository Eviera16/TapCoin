# Generated by Django 3.1.5 on 2024-01-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0030_auto_20240113_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='games',
            field=models.IntegerField(default=0, null=True, verbose_name='number of games'),
        ),
    ]
