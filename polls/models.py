from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from datetime import timedelta
from PIL import Image

# Create your models here.
class Theme(models.Model):
	name = models.CharField(max_length = 255, verbose_name = 'Название темы')
	image = models.ImageField(upload_to = 'images', verbose_name = 'Изображение', blank = True)
	description = models.TextField(blank = True, verbose_name = 'Описание')
	date_ended = models.DateTimeField(default = (timezone.now() + timedelta(days = 5)))
	date_started = models.DateTimeField(auto_now_add = True)
	users_voted = models.ManyToManyField(get_user_model(), blank = True, related_name = 'themes')

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('polls:theme_url', kwargs = {'theme_id': self.id})
	def get_count_url(self):
		return reverse('count:count_url', kwargs = {'id': self.id})

	class Meta:
		db_table = 'theme'
		ordering = ['date_ended']
		verbose_name = 'Тема'
		verbose_name_plural = 'Темы'

class Candidat(models.Model):
	theme = models.ForeignKey(Theme, on_delete = models.CASCADE, default = None)
	name = models.CharField(max_length = 255, verbose_name = 'Кандидат')
	image = models.ImageField(upload_to = 'photos', verbose_name = 'Фотография')
	move = models.CharField(max_length = 255, verbose_name = 'Описание')
	votes = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('polls:check_url', kwargs = {'theme_id': self.theme.id, 'can_id': self.id})
	def get_vote_url(self):
		return reverse('polls:vote_url', kwargs = {'theme_id': self.theme.id, 'can_id': self.id})

	class Meta:
		db_table = 'candidat'
		ordering = ['name']
		verbose_name = 'Кандидат'
		verbose_name_plural = 'Кандидаты'