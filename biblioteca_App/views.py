import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views import View
from .models import Libro, Prestamo
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)

class CancelarPrestamo(View):
    nombre_template = 'biblioteca_App/cancel_prestamo.html'
    

    def get(self, request, pk):
        prestamo = Prestamo.objects.get(id=pk)
        return render(request, self.nombre_template, { 'prestamo': prestamo})

    def post(self, request, pk):
        prestamo = Prestamo.objects.get(id=pk)
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion = datetime.datetime.now()
        prestamo.save()

        book = prestamo.libro
        book.disponibilidad = 'disponible'
        book.save()
        
        return redirect('list_my_books')

class PrestamoBook(View):
    nombre_template = 'biblioteca_App/confirm_prestamo.html'
    

    def get(self, request, pk):
        book = Libro.objects.get(id=pk)
        return render(request, self.nombre_template, { 'book': book})

    def post(self, request, pk):
        book = Libro.objects.get(id=pk)
        book.disponibilidad = 'prestado'
        book.save()
        prestamo = Prestamo()
        prestamo.libro = book
        prestamo.fecha_prestamo = datetime.date.today()
        prestamo.fecha_devolucion = datetime.datetime.now()
        prestamo.usuario = request.user
        prestamo.estado = 'prestado'
        prestamo.save()
        return redirect('list_books')


class ListBooks(ListView):
    model = Libro
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["libros_disponibles"] = Libro.objects.filter(disponibilidad="disponible")
        context["libros_prestados"] = Libro.objects.filter(disponibilidad="prestado")
        return context

    # def get_queryset(self):
    #     return Libro.objects.filter(disponibilidad="disponible")
    
    #queryset = Libro.objects.filter(disponibilidad="disponible")

class ListMyBooks(ListView):
    model = Prestamo
    template_name = 'biblioteca_App/list_my_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["libros_prestados"] = Prestamo.objects.filter(estado="prestado", usuario = self.request.user)
        context["libros_devueltos"] = Prestamo.objects.filter(estado="devuelto", usuario = self.request.user)
        return context

    # def get_queryset(self):
    #     return Libro.objects.filter(disponibilidad="disponible")
    
    #queryset = Libro.objects.filter(disponibilidad="disponible")


class DetailBook(DetailView):
    model = Libro

class DeleteBook(DeleteView):
    model = Libro
    success_url = reverse_lazy("list_books")

class EditBook(UpdateView):
    model = Libro
    fields = ['titulo', 'autores','editorial','fecha_publicacion', 'genero','isbn','resumen', 'disponibilidad', 'portada']
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("list_books")
    
class FormBooks(CreateView):
    model = Libro
    fields = ['titulo', 'autores','editorial','fecha_publicacion', 'genero','isbn','resumen', 'disponibilidad', 'portada']
    success_url = reverse_lazy("list_books")
