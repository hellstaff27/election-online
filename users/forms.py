from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import date, timedelta

class UserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']

class UserChangeForm(UserChangeForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']

class AuthForm(forms.Form):
	email = forms.CharField(max_length = 255, label = 'Эл. Почта', widget = forms.TextInput(attrs = {'class': 'form-control text-center', 'autofocus': True, 'placeholder': 'example@example.xyz}))
	password = forms.CharField(max_length = 255, label = 'Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control text-center'}))

	error_messages = {
		'password_mismatch': 'Неправильный пароль',
		'user_mismatch': 'Такого пользователя не обнаружено'
	}

class RegistForm(forms.ModelForm):
	password1 = forms.CharField(max_length = 255, label = 'Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control text-center'}))
	password2 = forms.CharField(max_length = 255, label = 'Подтвердите пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control text-center'}))

	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress']
		widgets = {
			'username': forms.TextInput(attrs = {'class': 'form-control text-center', 'autofocus': True, 'placeholder': 'Иванов Виктор Владимирович'}),
			'email': forms.EmailInput(attrs = {'class': 'form-control text-center', 'placeholder': 'your@mail.com'}),
			'ser': forms.NumberInput(attrs = {'class': 'form-control text-center', 'placeholder': '1448'}),
			'num': forms.NumberInput(attrs = {'class': 'form-control text-center', 'placeholder': '123456'}),
			'date': forms.DateInput(attrs = {'class': 'form-control text-center', 'placeholder': '1998-01-02'}),
			'given': forms.Textarea(attrs = {'class': 'form-control text-center', 'placeholder': 'МВД России по Чувашской Республике'}),
			'code': forms.TextInput(attrs = {'class': 'form-control text-center', 'placeholder': '123456'}),
			'adress': forms.TextInput(attrs = {'class': 'form-control text-center', 'placeholder': 'Чебоксары Гагарина 22 120'}),
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
					self.error_messages['password2']['password_mismatch'],
					code = 'password_mismatch',
					)
			return password2
		def clean_date(self):
			date = self.cleaned_data.get('date')
			if date and date > date.today() - timedelta(days = 6570):
				raise forms.ValidationError(
					self.error_messages['date']['date_mismatch'],
					code = 'date_mismatch'
					)
			return date
		def clean_ser(self):
			ser = self.cleaned_data.get('ser')
			if ser and len(str(ser)) != 4:
				raise forms.ValidationError(
					self.error_messages['ser']['ser_mismatch'],
					code = 'ser_mismatch'
					)
			return ser
		def clean_num(self):
			num = self.cleaned_data.get('num')
			if num and len(str(num)) != 6:
				raise forms.ValidationError(
					self.error_messages['num']['num_mismatch'],
					code = 'num_mismatch'
					)
			return num
		def clean_code(self):
			code = self.cleaned_data.get('code')
			if code and len(str(code)) != 6:
				raise forms.ValidationError(
					self.error_messages['code']['code_mismatch'],
					code = 'code_mismatch'
					)
			return code
		def clean_email(self):
			email = self.cleaned_data.get('email')
			if email and get_user_model().objects.filter(email = email).count():
				raise forms.ValidationError(
					error_messages['email']['email_mismatch'],
					code = 'email_mismatch'
					)
			return email
		def clean_username(self):
			username = self.cleaned_data.get('username')
			if username and username.lower() == 'adminn':
				raise forms.ValidationError(
					error_messages['not_allowed_name'],
					code = 'not_allowed_name'
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
