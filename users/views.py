from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import *
from .forms import AuthForm, RegistForm, ConfirmForm
from random import randint

# Create your views here.
def auth(request):
	own = 'users'
	if request.method == 'POST':
		form = AuthForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username = cd['email'], password = cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect(reverse('polls:index_url'))
				else:
					answer = 'Данный аккаунт является неактивным'
					return render(request, 'users/auth.html', {'form': form, 'answer': answer, 'own': own})
			else:
				answer = 'Такого аккаунта не найдено'
				return render(request, 'users/auth.html', {'form': form, 'answer': answer, 'own': own})
		else:
			answer = 'Данные не подлежать валидации'
			return render(request, 'users/auth.html', {'form': form, 'answer': answer, 'own': own})
	else:
		form = AuthForm()
		return render(request, 'users/auth.html', {'form': form, 'own': own})

def regist(request):
	own = 'users'
	if request.method == 'POST':
		form = RegistForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			User = get_user_model()
			user = authenticate(username = cd['email'], password = cd['password2'])
			try:
				check_user = User.objects.get(ser = cd['ser'], num = cd['num'])
			except User.DoesNotExist:
				check_user = None
			if user is None and check_user is None:
				request.session['new_user'] = cd
				request.session['confirm_code'] = randint(111111, 666666)
				message = render_to_string('users/email.html', {'code': request.session['confirm_code']})
				send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
				return redirect(reverse('users:check_email_url'))
			else:
				answer = 'Такой аккаунт уже существует'
				return render(request, 'users/regist.html', {'form': form, 'answer': answer, 'own': own})
		else:
			answer = 'Данные не подлежать валидации'
			return render(request, 'users/regist.html', {'form': form, 'answer': answer, 'own': own})
	else:
		form = RegistForm()
		return render(request, 'users/regist.html', {'form': form, 'own': own})

def check_email(request):
	own = 'users'
	if request.session.get('confirm_code', False):
		message = render_to_string('users/email.html', {'code': request.session['confirm_code']})
	else:
		return redirect(reverse('users:regist_url'))
	cd = request.session['new_user']
	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
			confirm = form.cleaned_data.get('confirm')
			if confirm == request.session['confirm_code']:
				user = User.objects.create_user(username = cd['username'], email = cd['email'], password = cd['password2'], date = cd['date'], ser = cd['ser'], \
					num = cd['num'], given = cd['given'], code = cd['code'], adress= cd['adress'])
				login(request, user)
				return redirect(reverse('polls:index_url'))
			else:
				send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
				form = ConfirmForm()
				answer = 'Неправильный код'
				return render(request, 'users/confirm.html', {'form': form, 'answer': answer})
		else:
			send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
			form = ConfirmForm()
			answer = 'Данные не валидны'
			return render(request, 'users/confirm.html', {'form': form, 'asnwer': answer})

	else:
		send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
		form = ConfirmForm()
		return render(request, 'users/confirm.html', {'form': form, 'own': own})
