# biblioteca_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser



class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/')


class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    sitio_web = models.URLField()

class Libro(models.Model):
    Disponibilidad = [('disponible', 'Disponible'),('prestado', 'Prestado'),('en_proceso', 'En proceso de préstamo'),]

    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=50)
    isbn = models.CharField(max_length=15)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=22, choices=Disponibilidad, default='disponible')
    portada = models.ImageField(upload_to='portadas/')

class Prestamo(models.Model):
    Estado = [('prestado', 'Prestado'),('devuelto', 'Devuelto'),]

    libro = models.CharField(max_length=200)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    usuario = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=Estado, default='prestado')

class Usuario(AbstractUser):
    dni = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10)
