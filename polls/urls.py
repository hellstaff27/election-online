from django.urls import path
from . import views

urlpatterns = [
	# path('', views.Auth.as_view(), name = 'auth_url'),
	path('', views.redirect_url, name = 'redirect_url'),
	path('index/', views.index, name = 'index_url'),
	path('auth/', views.auth, name = 'auth_url'),
	path('check/<int:id>', views.check, name = 'check_url'),
	path('vote/<int:id>', views.vote, name = 'vote_url'),
	path('voted/', views.voted, name = 'voted_url'),
]