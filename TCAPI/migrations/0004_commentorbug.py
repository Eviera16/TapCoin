# Generated by Django 3.1.5 on 2022-01-11 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0003_emailcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentOrBug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=150, verbose_name='CommentOrBug')),
                ('user', models.CharField(max_length=80, verbose_name='username')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
