# Generated by Django 2.0.1 on 2018-03-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20180306_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='answer_set',
        ),
        migrations.AddField(
            model_name='answerset',
            name='choices',
            field=models.ManyToManyField(to='polls.Choice'),
        ),
    ]