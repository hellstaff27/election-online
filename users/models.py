from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager

# Create your models here.
class User(AbstractUser):
	username = models.CharField(max_length = 255, verbose_name = 'Ф.И.О.')
	email = models.EmailField(verbose_name = 'email адрес', unique = True)
	ser = models.PositiveIntegerField(default = 0, verbose_name = 'Серия')
	num = models.PositiveIntegerField(default = 0, verbose_name = 'Номер')
	date = models.DateField(verbose_name = 'Дата рождения (в формате дд.мм.гггг)')
	given = models.TextField(blank = False, verbose_name = 'Кем выдан паспорт')
	code = models.PositiveIntegerField(default = 0, verbose_name = 'Код подразделения')
	adress = models.CharField(max_length = 255, verbose_name = 'Адрес прописки')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['date', 'username',]

	objects = UserManager()

	def __str__(self):
		return self.username

	class Meta:
		db_table = 'user'
		ordering = ['username']
		verbose_name = 'Голосующий'
		verbose_name_plural = 'Голосующие'