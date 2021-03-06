# Generated by Django 3.0.2 on 2020-01-20 13:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название темы')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('date_ended', models.DateTimeField(default=datetime.datetime(2020, 1, 25, 13, 37, 36, 737243, tzinfo=utc))),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('users_voted', models.ManyToManyField(blank=True, related_name='themes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
                'db_table': 'theme',
                'ordering': ['date_ended'],
            },
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Кандидат')),
                ('image', models.ImageField(upload_to='photos', verbose_name='Фотография')),
                ('move', models.CharField(max_length=255, verbose_name='Описание')),
                ('votes', models.PositiveIntegerField(default=0)),
                ('date_voted', models.DateTimeField(auto_now_add=True)),
                ('theme', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='polls.Theme')),
                ('voter', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Кандидат',
                'verbose_name_plural': 'Кандидаты',
                'db_table': 'candidat',
                'ordering': ['name'],
            },
        ),
    ]
