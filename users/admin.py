from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import *

# Register your models here.
class UserAdmin(UserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	model = UserAdmin
	list_displays = ['username', 'ser', 'num', 'email', 'is_staff', 'is_active',]
	list_filter = ['username', 'ser', 'num', 'email', 'is_staff', 'is_active',]
	fieldsets = [
		[None, {'fields': ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress', 'password']}],
		['Permissions', {'fields': ['is_staff', 'is_active']}],
	]
	add_fieldsets = [
		 [None, {
            'classes': ['wide',],
            'fields': ['username', 'email', 'ser', 'num', 'date', 'given', 'code', 'adress', 'password1', 'password2', 'is_staff', 'is_active']}
        ],
	]
	search_fields = ['ser', 'num', 'email', 'username']
	ordering = ['username',]

admin.site.register(User, UserAdmin)