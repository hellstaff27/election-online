from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
	path('', views.Auth.as_view(), name = 'auth_url'),
	path('regist/', views.Regist.as_view(), name = 'regist_url'),
	# path('check_email/', views.check_email , name = 'check_email_url'),
	path('logout', auth_views.LogoutView.as_view(), name = 'logout_url'),
]