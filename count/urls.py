from django.urls import path
from . import views

app_name = 'count'
urlpatterns = [
	path('', views.index, name = 'index_url'),
	path('<int:id>', views.count, name = 'count_url')
]