# biblioteca_app/admin.py
from django.contrib import admin
from .models import Usuario, Libro
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario,UserAdmin)
admin.site.register(Libro)

