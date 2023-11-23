# biblioteca_app/admin.py
from django.contrib import admin
from .models import Usuario, Autor, Editorial, Libro, Prestamo

admin.site.register(Usuario)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Libro)
admin.site.register(Prestamo)
