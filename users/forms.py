from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

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
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'your@mail.com', 'autofocus': True}), max_length = 255, label = 'E-mail')
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'form-control'}), max_length = 255, label = 'Пароль')

class RegistForm(forms.Form):
	username = forms.CharField(max_length = 255, label = 'Ф.И.О.', widget = forms.TextInput(attrs = {'class': 'form-control', 'autofocus': True, 'placeholder': 'Иванов Виктор Владимирович'}))
	email = forms.EmailField(max_length = 255, label = 'E-mail', widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'your@mail.com'}))
	ser = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '1448'}), label = 'Серия паспорта')
	num = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '123456'}), label = 'Номер паспорта')
	date = forms.DateField(widget = forms.DateInput(attrs = {'class': 'form-control', 'placeholder': '1998-01-02'}), label = 'Дата рождения (формат: гггг-мм-дд)')
	given = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'МВД России по Чувашской Республике'}), label = 'Кем выдан паспорт')
	code = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '123456'}), label = 'Код подразделения')
	adress = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Чебоксары Гагарина 11 23', 'autocomplete': False}), label = 'Адрес прописки')
	password1 = forms.CharField(max_length = 255, label = 'Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
	password2 = forms.CharField(max_length = 255, label = 'Подтвердите пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))

	error_messages = {
		'password_mismatch': 'Пароли не сходятся',
		'date_mismatch': 'Ваш возраст слишком мал',
		# 'ser_and_num_mismatch': 'Такая серия и номер паспорта уже принадлежат одному гражданину',
		'ser_mismatch': 'Неправильный формат серии',
		'num_mismatch': 'Неправильный формат номера',
		'code_mismatch': 'Неправильный формат кода подразделения',
	}

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code = 'password_mismatch',
				)
		return password2
	def clean_date(self):
		date = self.cleaned_data.get('date')
		if date and date > date.today() - timedelta(days = 6570):
			raise forms.ValidationError(
				self.error_messages['date_mismatch'],
				)
		return date
	def clean_ser(self):
		ser = self.cleaned_data.get('ser')
		if ser and len(str(ser)) != 4:
			raise forms.ValidationError(
				self.error_messages['ser_mismatch']
				)
		return ser
	def clean_num(self):
		num = self.cleaned_data.get('num')
		if num and len(str(num)) != 6:
			raise forms.ValidationError(
				self.error_messages['num_mismatch']
				)
		return num
	def clean_code(self):
		code = self.cleaned_data.get('code')
		if code and len(str(code)) != 6:
			raise forms.ValidationError(
				self.error_messages['code_mismatch']
				)
		return code

class ConfirmForm(forms.Form):
	confirm = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'autofocus': True}), label = 'Код подтверждения')

	error_messages = {
		'confirm_mismatch': 'Код введён неверно'
	}

	def clean_confirm(self):
		confirm = self.cleaned_data.get('confirm')
		if confirm and len(str(confirm)) != 6:
			raise form.ValidationError(
				self.error_messages['confirm_mismatch']
				)
		return confirm