# biblioteca_app/admin.py
from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario,UserAdmin)

