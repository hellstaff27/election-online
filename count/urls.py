from django.urls import path
from . import views

urlpatterns = [
	path('', views.count, name = 'count_url'),
]