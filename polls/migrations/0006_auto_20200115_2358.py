# Generated by Django 2.2.7 on 2020-01-15 20:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200115_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 20, 20, 58, 46, 55429, tzinfo=utc)),
        ),
        migrations.AlterModelTable(
            name='candidat',
            table='candidat',
        ),
        migrations.AlterModelTable(
            name='theme',
            table='theme',
        ),
    ]