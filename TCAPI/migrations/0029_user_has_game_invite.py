# Generated by Django 3.1.5 on 2024-01-07 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0028_auto_20231209_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_game_invite',
            field=models.BooleanField(default=False, verbose_name='has a game invite'),
        ),
    ]