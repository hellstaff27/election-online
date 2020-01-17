from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from polls.models import *

# Create your views here.
def index(request):
	themes = Theme.objects.all()
	time = timezone.now()
	own = 'count'
	return render(request, 'index.html', {'themes': themes, 'time': time, 'own': own})

def count(request, id):
	theme = Theme.objects.get(pk = id)
	own = 'count'
	if theme.date_ended < timezone.now():
		candidats = theme.candidat_set.order_by('-votes')
		return render(request, 'count.html', {'candidats': candidats, 'own': own})
	else:
		return redirect(reverse('count:index_url'))