from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# from django.db.models import query
# from django.utils.timezone import now
from .models import *
from .forms import *

# Create your views here.
def auth(request):
	# if not request.session['access']:
		# if not request.session['tries']:
		# 	request.session['tries'] = 
		# else:
		# 	request.session['tries'] += 1
		# if request.session['tries'] > 4:
		# 	return render(request, 'toomany.html', {})
		# image = Service.objects.
	if request.session.get('vote', False):
		request.session['vote'] = False
	if not request.session.get('access', True):
		return render(request, 'polls/wait.html', {})
	if request.method == 'POST':
		form = VoterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				voter = Voter.objects.get(ser = cd['ser'], num = cd['num'])			#ищу юзера
			except :
				# answer = 'Таких паспорт данных нет'
				# return render(request, 'polls/auth.html', {'form': form, 'answer': answer})
				voter = False
			if voter and voter.name == cd['name'].lower() and voter.date == cd['date'] and voter.given == cd['given'].lower() \
			and voter.code == cd['code'] and voter.adress == cd['adress'].lower():
				if voter.voted == False:
					request.session['access'] = True
					request.session['vote'] = 0
					request.session['voter'] = voter.ser, voter.num
					return redirect(reverse('index_url'))#редирект на страницу выбора
				else:
					answer = 'Данный человек уже проголосовал'
					return render(request, 'polls/auth.html', {'form': form, 'answer': answer})
			else:
				answer = 'Введённые данные не существуют'   #Таких паспортных данных нет 
				return render(request, 'polls/auth.html', {'form': form, 'answer': answer})
		else:
			answer = 'Введённые данные неверны'   #не валидны
			return render(request, 'polls/auth.html', {'form': form, 'answer': answer})
	else:
		form = VoterForm()
		return render(request, 'polls/auth.html', {'form': form})
	# else:
	# 	return render(request, 'wait.html', {})

def index(request):
	# if not request.session['access']:
	# 	return render(request, '')
	if request.session.get('vote', False):
		request.session['vote'] = False
	if request.session.get('access', False):
		candidats = Candidat.objects.all()
		return render(request, 'polls/index.html', {'candidats': candidats})		#вот и помер дед максим...
	elif not request.session.get('access', True):
		return render(request, 'polls/wait.html', {})
	else:
		return render(request, 'polls/login.html', {})
		# return redirect(reverse('auth_url'))

def check(request, id):
	if request.session.get('access', False):
		candidat = get_object_or_404(Candidat, pk = id)
		request.session['vote'] = id
		return render(request, 'polls/check.html', {'candidat': candidat})
	elif not request.session.get('access', True):
		return render(request, 'polls/wait.html', {})
	else:
		# return render(request, 'polls/login.html', {})
		return redirect(reverse('index_url'))

def vote(request, id):
	if request.session.get('access', False):
		if request.session.get('vote', False):
			if request.session['vote'] == id:
				candidat = get_object_or_404(Candidat, pk = id)
				candidat.votes += 1
				candidat.save()
				voter = Voter.objects.get(ser = request.session['voter'][0], num = request.session['voter'][1])
				voter.voted = True
				voter.save()
				request.session['access'] = False
				del request.session['voter']
				del request.session['vote']
				request.session.set_expiry(30)
				return redirect(reverse('voted_url'))
			else:
				return redirect(reverse('check_url', kwargs = {'id': id}))
		else:
			candidats = Candidat.objects.all()
			return render(request, 'polls/index.html', {'candidats': candidats})
	elif not request.session.get('access', True):
		return render(request, 'polls/wait.html', {})
	else:
		# return render(request, 'polls/login.html', {})
		return redirect(reverse('index_url'))

	# else:
	# 	return render(request, '', {})

def voted(request):
	if request.session.get('vote', False):
		del request.session['vote']
	if not request.session.get('access', True):
		# if not request.session.get('vote', True):
		return render(request, 'polls/voted.html', {})
	return redirect(reverse('index_url'))

def redirect_url(request):
	return redirect(reverse('auth_url'))

def handler404(request, exception):
	return render(request, 'errors/404.html', {}, status = 404)

def handler400(request, exception):
	return render(request, 'errors/400.html', {}, status = 400)

def handler500(request):
	return render(request, 'errors/500.html', {}, status = 500)

