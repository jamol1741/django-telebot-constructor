# Generated by Django 3.2.8 on 2021-10-27 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bot',
        ),
        migrations.AddField(
            model_name='user',
            name='bot',
            field=models.ManyToManyField(to='bots.Bot'),
        ),
    ]
