from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404

from .models import *

from django.utils import timezone

# Create your views here.
def index(request):
	# if request.session.get('vote', False):
	# 	del request.session['vote']
	themes = Theme.objects.order_by('-id')
	time = timezone.now()
	own = 'polls'
	return render(request, 'polls/index.html', {'themes': themes, 'time': time, 'own': own})

def theme(request, theme_id):
	# if request.session.get('vote', False):
	# 	del request.session['vote']
	candidats = Candidat.objects.filter(theme__id = theme_id) or False
	theme = get_object_or_404(Theme, pk = theme_id)
	own = 'polls'
	if request.user.is_authenticated:
		voted = theme.users_voted.filter(id = request.user.id)
	else:
		voted = True
	time = timezone.now()
	date_ended = theme.date_ended
	return render(request, 'polls/list.html', {'candidats': candidats, 'voted': voted, 'own': own, 'time': time, 'date_ended': date_ended})

def check(request, theme_id, can_id):
	theme = get_object_or_404(Theme, pk = theme_id)
	own = 'polls'
	try:
		candidat = theme.candidat_set.get(pk = can_id)
	except candidat.DoesNotExist:
		raise Http404('Такого варианта нет')
	if request.user.is_authenticated:
		voted = theme.users_voted.filter(id = request.user.id)
		if not voted:
			request.session['vote'] = [theme_id, can_id]
	else:
		voted = True
	time = timezone.now()
	date_ended = theme.date_ended
	return render(request, 'polls/check.html', {'candidat': candidat, 'voted': voted, 'own': own, 'time': time, 'date_ended': date_ended})

def vote(request, theme_id, can_id):
	if request.session.get('vote', False):
		if request.session['vote'][0] == theme_id and request.session['vote'][1] == can_id:
			theme = Theme.objects.get(pk = theme_id)
			candidat = theme.candidat_set.get(id = can_id)
			candidat.votes += 1
			candidat.save()
			theme.users_voted.add(request.user.id)
			theme.save()
			del request.session['vote']
			return redirect(reverse('polls:voted_url', kwargs = {'id': theme_id}))
		else:
			return redirect(reverse('polls:check_url', kwargs = {'theme_id': theme_id, 'can_id': can_id}))
	else:
		return redirect(reverse('polls:index_url'))

def voted(request, id):
	# if request.session.get('vote', False):
	# 	del request.session['vote']
	own = 'polls'
	if request.user.is_authenticated:
		theme = get_object_or_404(Theme, pk = id)
		voted = theme.users_voted.get(id = request.user.id) or False
		if theme is not None and voted:
			return render(request, 'polls/voted.html', {'own': own})
	return redirect(reverse('polls:index_url'))



def handler404(request, exception):
	return render(request, 'errors/404.html', status = 404)