# biblioteca_app/admin.py
from django.contrib import admin
from .models import Usuario, Libro, Prestamo, Autor, Editorial
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario,UserAdmin)
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(Autor)
admin.site.register(Editorial)
