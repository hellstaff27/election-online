from django.db import models
# from django.contrib.auth.models import AbstractUser
from .models import *
from PIL import Image

# Create your models here.
class Candidat(models.Model):
	name = models.CharField(max_length = 255, verbose_name = 'Имя кандидата')
	image = models.ImageField(upload_to = 'photos', verbose_name = 'Фотография')
	move = models.CharField(max_length = 255, verbose_name = 'Выдвеженец')
	votes = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = 'Кандидат'
		verbose_name_plural = 'Кандидаты'

class Voter(models.Model):
	name = models.CharField(max_length = 255, verbose_name = 'Ф.И.О.')
	ser = models.PositiveIntegerField(default = 0000, verbose_name = 'Серия')
	num = models.PositiveIntegerField(default = 000000, verbose_name = 'Номер')
	date = models.DateField(verbose_name = 'Дата рождения (в формате дд.мм.гггг)')
	given = models.TextField(blank = False, verbose_name = 'Кем выдан паспорт')
	code = models.PositiveIntegerField(default = 000000, verbose_name = 'Код подразделения')
	adress = models.CharField(max_length = 255, verbose_name = 'Адрес прописки')
	voted = models.BooleanField(default = False, verbose_name = 'Голос')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = 'Голосующий'
		verbose_name_plural = 'Голосующие'

# class User():
# 	def __init__(self, ):
# 		self. =
# 		super().__inti__()

# class Service(models.Model):
# 	image = models.ImageField(upload_to = 'service', verbose_name = 'Служебная картинка')

# 	def __str__(self):
# 		return self.image.verbose_name

# 	class Meta:
# 		ordering = ['image']
# 		verbose_name = 'Служебная картинка'
# 		verbose_name_plural = 'Служебные картинки'
