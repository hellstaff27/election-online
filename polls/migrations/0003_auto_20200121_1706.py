# Generated by Django 3.0.2 on 2020-01-21 14:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200120_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 26, 14, 6, 54, 303735, tzinfo=utc)),
        ),
    ]