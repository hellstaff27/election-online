from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

# Create your models here.
class User(AbstractUser):
	# username = models.CharField(max_length = 255, verbose_name = 'Ф.И.О.')
	username = models.CharField(verbose_name = 'Имя', unique = True, max_length = 255)
	email = models.EmailField(verbose_name = 'email адрес', blank = True, max_length = 255,)
	ser = models.CharField(default = 0, verbose_name = 'Серия', max_length = 255,)
	num = models.CharField(default = 0, verbose_name = 'Номер', max_length = 255,)
	date = models.CharField(verbose_name = 'Дата рождения (в формате дд.мм.гггг)', max_length = 255,)
	given = models.CharField(blank = False, verbose_name = 'Кем выдан паспорт', max_length = 255,)
	code = models.CharField(default = 0, verbose_name = 'Код подразделения', max_length = 255,)
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