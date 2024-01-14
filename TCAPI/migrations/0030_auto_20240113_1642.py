# Generated by Django 3.1.5 on 2024-01-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCAPI', '0029_user_has_game_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='friendmodel',
            name='receiving_user',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='friendmodel',
            name='sending_user',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='first',
            field=models.CharField(max_length=80, null=True, verbose_name='first player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='second',
            field=models.CharField(max_length=80, null=True, verbose_name='second player'),
        ),
        migrations.AlterField(
            model_name='gameinvite',
            name='reciever',
            field=models.CharField(max_length=80, null=True, verbose_name='reciever'),
        ),
        migrations.AlterField(
            model_name='gameinvite',
            name='sender',
            field=models.CharField(max_length=80, null=True, verbose_name='sender'),
        ),
        migrations.AlterField(
            model_name='league',
            name='league_title',
            field=models.CharField(max_length=80, null=True, verbose_name='league title'),
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='userssecurityquestionsanswers',
            name='answer_1',
            field=models.CharField(max_length=160, null=True, verbose_name='answer one'),
        ),
        migrations.AlterField(
            model_name='userssecurityquestionsanswers',
            name='answer_2',
            field=models.CharField(max_length=160, null=True, verbose_name='answer two'),
        ),
        migrations.AlterField(
            model_name='userssecurityquestionsanswers',
            name='question_1',
            field=models.CharField(max_length=160, null=True, verbose_name='question one'),
        ),
        migrations.AlterField(
            model_name='userssecurityquestionsanswers',
            name='question_2',
            field=models.CharField(max_length=160, null=True, verbose_name='question two'),
        ),
    ]
