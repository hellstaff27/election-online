from django import forms
from .models import *

# class VoterForm(forms.ModelForm):
# 	class Meta:
# 		model = Voter
# 		fields = {
# 			'name': forms.TextInput(attrs = {'maxlength': 255}),
# 			'ser': forms.NumberInput(attrs = {}),
# 			'num': forms.NumberInput(attrs = {}),
# 			'date': forms.DateInput(attrs = {}),
# 			'given': forms.Textarea(attrs = {}),
# 			'code': forms.NumberInput(attrs = {}),
# 			'adress': forms.TextInput(attrs = {'maxlength': 255}),
# 		}

class VoterForm(forms.Form):
	name = forms.CharField(max_length = 255, label = 'Ф.И.О.', widget = forms.TextInput(attrs = {'class': 'form-control', 'autofocus': True, 'placeholder': 'Иванов Виктор Владимирович'}))
	ser = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '1448'}), label = 'Серия паспорта')
	num = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '123456'}), label = 'Номер паспорта')
	date = forms.DateField(widget = forms.DateInput(attrs = {'class': 'form-control', 'placeholder': '1998-01-02'}), label = 'Дата рождения (формат: гггг-мм-дд)')
	given = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'МВД России по Чувашской Республике'}), label = 'Кем выдан паспорт')
	code = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '123456'}), label = 'Код подразделения')
	adress = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Чебоксары Гагарина 11 23', 'autocomplete': False}), label = 'Адрес прописки')
