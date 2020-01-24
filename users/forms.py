from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import datetime

class UserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']

class UserChangeForm(UserChangeForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']

class AuthForm(forms.Form):
	email = forms.CharField(max_length = 255, label = 'Ваш e-mail', widget = forms.EmailInput(attrs = {'class': 'form-control', 'autofocus': True, 'placeholder': 'your@mail.com'}))
	password = forms.CharField(max_length = 255, label = 'Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))

	error_messages = {
		'password_mismatch': 'Неправильный пароль',
		'user_mismatch': 'Такого пользователя не обнаружено'
	}

class RegistForm(forms.ModelForm):
	password1 = forms.CharField(max_length = 255, label = 'Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
	password2 = forms.CharField(max_length = 255, label = 'Подтвердите пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))

	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']
		widgets = {
			'username': forms.TextInput(attrs = {'class': 'form-control', 'autofocus': True, 'placeholder': 'Иванов Виктор Владимирович'}),
			'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'your@mail.com'}),
			'ser': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '1448', 'maxlength' : 4, 'pattern' : '\d*'}),
			'num': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '123456', 'maxlength' : 6, 'pattern' : '\d*'}),
			'date': forms.DateInput(attrs = {'class': 'form-control', 'placeholder': '1998-01-02'}),
			'given': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'МВД России по Чувашской Республике'}),
			'code': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '123456', 'maxlength' : 6, 'pattern' : '\d*'}),
			'adress': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Чебоксары Гагарина 22 120'}),
		}
		labels = {
			'username': _('Ваше имя'),
			'email': _('Ваш e-mail'),
			'ser': _('Ваша серия'),
			'num': _('Ваш номер'),
			'date': _('Дата рождения (формат: гггг-мм-дд)'),
			'given': _('Кем выдан паспорт'),
			'code': _('Ваш код подразделения'),
			'adress': _('Ваш адрес прописки'),
			'password1': _('Ваш пароль'),
			'password2': _('Подтвердите пароль'),
		}

	error_messages = {
		'password2': {
			'password_mismatch': 'Пароли не сходятся',
		},
		'date': {
			'date_mismatch': 'Ваш возраст слишком мал'
		},
		'ser': {
			'ser_mismatch': 'Неправильный формат серии',
		},
		'num': {
			'num_mismatch': 'Неправильный формат номера',
		},
		'code': {
			'code_mismatch': 'Неправильный формат кода подразделения',
		},
		'email': {
			'email_mismatch': 'Такой e-mail уже занят',
		},
		'username': {
			'not_allowed_name': 'Нельзя иметь аккаунт с таким именем',
		} 
	}

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				# error_messages['password2']['password_mismatch'],
				# code = 'password_mismatch',
				'Пароли не сходятся'
				)
		return password2
	def clean_date(self):
		date = self.cleaned_data.get('date')
		date = [int(i) for i in date.split('-')]
		if date and datetime.date(year = date[0], month = date[1], day = date[2]) > datetime.date.today():
			raise forms.ValidationError(
				'Такой даты ещё не было'
				)
		elif date and datetime.date(year = date[0], month = date[1], day = date[2]) > datetime.date.today() - datetime.timedelta(days = 6570):
			raise forms.ValidationError(
				# error_messages['date']['date_mismatch'],
				# code = 'date_mismatch'
				'Ваш возраст слишком мал'
				)
		return date
	def clean_ser(self):
		ser = self.cleaned_data.get('ser')
		if ser and len(str(ser)) != 4:
			raise forms.ValidationError(
				# error_messages['ser']['ser_mismatch'],
				# code = 'ser_mismatch'
				'Неправильный формат серии'
				)
		return ser
	def clean_num(self):
		num = self.cleaned_data.get('num')
		if num and len(str(num)) != 6:
			raise forms.ValidationError(
				# error_messages['num']['num_mismatch'],
				# code = 'num_mismatch'
				'Неправильный формат номера'
				)
		return num
	def clean_code(self):
		code = self.cleaned_data.get('code')
		if code and len(str(code)) != 6:
			raise forms.ValidationError(
				# error_messages['code']['code_mismatch'],
				# code = 'code_mismatch'
				'Неправильный формат кода подразделения'
				)
		return code
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email and get_user_model().objects.filter(email = email).count():
			raise forms.ValidationError(
				# error_messages['email']['email_mismatch'],
				# code = 'email_mismatch'
				'Такой e-mail уже занят'
				)
		return email
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if username and username.lower() == 'admin':
			raise forms.ValidationError(
				# error_messages['not_allowed_name'],
				# code = 'not_allowed_name'
				'Нельзя иметь аккаунт с таким именем'
				)
		return username

# class ConfirmForm(forms.Form):
# 	confirm = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'autofocus': True}), label = 'Код подтверждения')

# 	error_messages = {
# 		'confirm_mismatch': 'Код введён неверно'
# 	}

# 	def clean_confirm(self):
# 		confirm = self.cleaned_data.get('confirm')
# 		if confirm and len(str(confirm)) != 6:
# 			raise forms.ValidationError(
# 				self.error_messages['confirm_mismatch']
# 				)
# 		return confirm