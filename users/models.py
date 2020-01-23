from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

# Create your models here.
class User(AbstractUser):
	# username = models.CharField(max_length = 255, verbose_name = 'Ф.И.О.')
	username = models.CharField(verbose_name = 'Имя', unique = True, max_length = 255)
	email = models.EmailField(verbose_name = 'email адрес', max_length = 255,)
	ser = models.TextField(verbose_name = 'Серия')
	num = models.TextField(verbose_name = 'Номер')
	date = models.CharField(verbose_name = 'Дата рождения (в формате дд.мм.гггг)', max_length = 255,)
	given = models.CharField(blank = False, verbose_name = 'Кем выдан паспорт', max_length = 255,)
	code = models.TextField(verbose_name = 'Код подразделения')
	adress = models.CharField(max_length = 255, verbose_name = 'Адрес прописки')

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['date', 'email']

	objects = UserManager()

	def __str__(self):
		return self.username

	class Meta:
		db_table = 'user'
		ordering = ['username']
		verbose_name = 'Голосующий'
		verbose_name_plural = 'Голосующие'