from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
# from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import *

from django.utils import timezone
import json

# Create your views here.
def index(request):
	if request.session.get('vote', False):
		del request.session['vote']
	themes = Theme.objects.order_by('-id')
	time = timezone.now()
	return render(request, 'polls/index.html', {'themes': themes, 'time': time})

def theme(request, theme_id):
	if request.session.get('vote', False):
		del request.session['vote']
	theme = get_object_or_404(Theme, pk = theme_id)
	candidats = theme.candidat_set.filter(theme__id = theme_id)
	if request.user.is_authenticated:
		voted = theme.users_voted.filter(id = request.user.id)
	else:
		voted = True
	time = timezone.now()
	date_ended = theme.date_ended
	response = render(request, 'polls/list.html', {'candidats': candidats, 'voted': voted, 'time': time, 'date_ended': date_ended})
	return response

def check(request, theme_id, can_id):
	theme = get_object_or_404(Theme, pk = theme_id)
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
	return render(request, 'polls/check.html', {'candidat': candidat, 'voted': voted, 'time': time, 'date_ended': date_ended})

def vote(request, theme_id, can_id):
	if request.session.get('vote', False):
		if request.session['vote'][0] == theme_id and request.session['vote'][1] == can_id:
			theme = Theme.objects.get(pk = theme_id)
			candidat = theme.candidat_set.get(id = can_id)
			candidat.votes += 1
			candidat.save()
			theme.users_voted.add(request.user)
			theme.save()
			request.user.datevoted_set.create(candidat = candidat.name)
			del request.session['vote']
			return redirect(reverse('polls:voted_url', kwargs = {'id': theme_id}))
		else:
			return redirect(reverse('polls:check_url', kwargs = {'theme_id': theme_id, 'can_id': can_id}))
	else:
		return redirect(reverse('polls:index_url'))

def voted(request, id):
	if request.session.get('vote', False):
		del request.session['vote']
	if request.user.is_authenticated:
		theme = get_object_or_404(Theme, pk = id)
		voted = theme.users_voted.get(id = request.user.id) or False
		if theme is not None and voted:
			return render(request, 'polls/voted.html', {})
	return redirect(reverse('polls:index_url'))


# @csrf_exempt
# def votes(request):
# 	if request.is_ajax() and request.method == 'POST':
# 		if request.user.is_authenticated:
# 			votes = request.user.datevoted_set.order_by('-date_voted')
# 			if votes:
# 				message = serializers.serialize('json', votes),
# 				return HttpResponse(
# 					json.dumps({
# 						'message': render_to_string('includes/votes_list.html', {'votes': votes})
# 					}),
# 					content_type = 'application/json'
# 					)
# 			else:
# 				return HttpResponse(json.dumps({'message': 'Вы пока не голосовали'}))
# 		else:
# 			return HttpResponse(json.dumps({'message': 'Войдите в аккаунт'}))
# 	else:
# 		return HttpResponse(json.dumps({'message': 'Ошибка отправки данных'}))


def handler404(request, exception):
	return render(request, 'errors/404.html', status = 404)