from django.shortcuts import render
from polls.models import Candidat

# Create your views here.
def count(request):
	candidats = Candidat.objects.all()
	return render(request, 'count.html', {'candidats': candidats})