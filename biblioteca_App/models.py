# biblioteca_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser



class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/')
    
    def __str__(self):
        return self.nombre


class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    sitio_web = models.URLField()


    def __str__(self):
        return self.nombre

class Libro(models.Model):
    Disponibilidad = [('disponible', 'Disponible'),('prestado', 'Prestado'),('en_proceso', 'En proceso de préstamo'),]

    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor)
    editorial = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()

    GENEROS = (
            ('N', 'Novela'),
            ('C', 'Cuento'),
            ('P', 'Poesía'),
            ('T', 'Teatro'),
            ('O', 'Otros'),
        )

    genero = models.CharField(max_length=1, choices=GENEROS)
    isbn = models.CharField(max_length=15)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=22, choices=Disponibilidad, default='disponible')
    portada = models.ImageField(upload_to='portadas/')


    def __str__(self):

        return self.titulo




class Usuario(AbstractUser):
    dni = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10)

class Prestamo(models.Model):
    Estado = [('prestado', 'Prestado'),('devuelto', 'Devuelto'),]

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=Estado, default='prestado')