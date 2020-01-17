from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
	path('', views.index, name = 'index_url'),
	path('<int:theme_id>/', views.theme, name = 'theme_url'),
	path('<int:theme_id>/check/<int:can_id>/', views.check, name = 'check_url'),
	path('<int:theme_id>/vote/<int:can_id>/', views.vote, name = 'vote_url'),
	path('voted/<int:id>/', views.voted, name = 'voted_url'),
]