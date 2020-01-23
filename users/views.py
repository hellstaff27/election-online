from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import CreateView, View
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template.loader import render_to_string

from .models import *
from .forms import AuthForm, RegistForm
# from random import randint
import hashlib

# Create your views here.
class Auth(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			form = AuthForm()
			return render(request, 'users/auth.html', {'form': form})
		else:
			return redirect(reverse('polls_index_url'))
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			if request.method == 'POST':
				form = AuthForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					password = str(hashlib.sha256(str(cd['password']).encode('utf-8')).hexdigest())
					email = str(hashlib.sha256(str(cd['email']).encode('utf-8')).hexdigest())
					# for i,v in cd.items():
					# 	new_cd[i] = hashlib.sha256(str(v).encode('utf-8')).hexdigest()
					user = authenticate(request, email = email, password = password, username = None)
					if user is not None:
						if user.is_active:
							login(request, user)
							return redirect(reverse('polls:index_url'))
						else:
							answer = 'Данный аккаунт является неактивным'
							return render(request, 'users/auth.html', {'form': form, 'answer': answer})
					else:
						answer = 'Такого аккаунта не найдено'
						return render(request, 'users/auth.html', {'form': form, 'answer': answer})
				else:
					return render(request, 'users/auth.html', {'form': form})
			else:
				form = AuthForm()
				return render(request, 'users/auth.html', {'form': form})
		else:
			return redirect(reverse('polls:index_url'))

class Regist(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			form = RegistForm()
			return render(request, 'users/regist.html', {'form': form})
		else:
			return redirect(reverse('polls:index_url'))

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			if request.method == 'POST':
				form = RegistForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					new_cd = {}
					for i,v in cd.items():
						new_cd[i] = hashlib.sha256(str(v).encode('utf-8')).hexdigest()
					user = authenticate(username = new_cd['username'], password = new_cd['password2'])
					try:
						check_user = get_user_model().objects.get(ser = cd['ser'], num = cd['num'])
					except User.DoesNotExist:
						check_user = None
					if user is None and check_user is None: 
						user = get_user_model().objects.create_user(username = cd['username'], email = new_cd['email'], password = new_cd['password2'], date = new_cd['date'], ser = new_cd['ser'], \
							num = new_cd['num'], given = new_cd['given'], code = new_cd['code'], adress= new_cd['adress'])
						login(request, user)
						return redirect(reverse('polls:index_url'))
					else:
						answer = 'Аккаунт с такими данными уже существует'
						return render(request, 'users/regist.html', {'form': form, 'answer': answer})
				else:
					return render(request, 'users/regist.html', {'form': form})
			else:
				form = RegistForm()
				return render(request, 'users/regist.html', {'form': form})
		else:
			return redirect(reverse('polls:index_url'))







# request.session['new_user'] = cd
# request.session['confirm_code'] = randint(111111, 666666)
# return redirect(reverse('users:check_email_url'))

# def check_email(request):
# 	check_code = request.session.get('confirm_code')
# 	if request.session.get('confirm_code', False):
		# check_code = request.session['confirm_code']
		# message = render_to_string('users/email.html', {'code': check_code})
# 		request.session['confirm_code'] = randint(111111, 666666)
# 	else:
# 		return redirect(reverse('users:regist_url'))
# 	cd = request.session['new_user']
# 	if request.method == 'POST':
# 		form = ConfirmForm(request.POST)
# 		if form.is_valid():
# 			confirm = form.cleaned_data.get('confirm')
# 			if confirm == check_code:
# 				user = User.objects.create_user(username = cd['username'], email = cd['email'], password = cd['password2'], date = cd['date'], ser = cd['ser'], \
# 					num = cd['num'], given = cd['given'], code = cd['code'], adress= cd['adress'])
# 				del request.session['confirm_code']
# 				del request.session['new_user']
# 				login(request, user)
# 				return redirect(reverse('polls:index_url'))
# 			else:
# 				send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
# 				form = ConfirmForm()
# 				answer = 'Неправильный код'
# 				return render(request, 'users/confirm.html', {'form': form})
# 		else:
# 			send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
# 			form = ConfirmForm()
# 			answer = 'Данные не валидны'
# 			return render(request, 'users/confirm.html', {'form': form})
# 	else:
# 		send_mail('Проверка почты', message, settings.EMAIL_HOST_USER, [cd['email'],],)
# 		form = ConfirmForm()
# 		return render(request, 'users/confirm.html', {'form': form})