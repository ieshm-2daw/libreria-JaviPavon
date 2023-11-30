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
        book = Libro.objects.get(id=pk)
        return render(request, self.nombre_template, { 'book': book})

    def post(self, request, pk):
        book = Libro.objects.get(id=pk)
        book.disponibilidad = 'disponible'
        book.save()
        
        return redirect('list_books')

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
        prestamo.libro = book.titulo
        prestamo.fecha_prestamo = datetime.datetime.now()
        prestamo.fecha_devolucion = datetime.datetime.now()
        prestamo.usuario = request.user
        prestamo.save()
        return redirect('list_books')


class ListBooks(ListView):
    model = Libro
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["libros_disponibles"] = Libro.objects.filter(disponibilidad="disponible")
        context["libros_prestados"] = Libro.objects.filter(disponibilidad="prestado")
        context["libros_en_proceso"] = Libro.objects.filter(disponibilidad="en_proceso")
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
