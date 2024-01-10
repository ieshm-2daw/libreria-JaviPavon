import datetime
from typing import Any
from django.db.models.query import QuerySet 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .forms import ReviewForm
from django.views import View
from .models import Libro, Prestamo, Review
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


class ListBooks(LoginRequiredMixin, ListView):
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


class ReviewBook(View):
    model = Review
    template_name = 'biblioteca_App/reviews.html'
    

    def get(self, request, pk):
        libro = Libro.objects.get(pk=pk)
        review = Review.objects.filter(libro=libro)
        return render(request, self.template_name, { 'review': review, 'libro': libro})
    
class CreateReview(CreateView):
    model = Review
    template_name = 'biblioteca_App/create_review.html'
    fields = ['opinion']
    success_url = reverse_lazy("list_books")

    def get(self, request, pk):
        usuario = self.request.user
        libro = Libro.objects.get(pk=pk)
        review = Review.objects.filter(libro=libro, usuario=usuario).first()

        if review:
            form = ReviewForm(instance=review)
        else:
            form = ReviewForm()

        return render(request, self.template_name, {'review': review, 'libro': libro, 'form': form, 'usuario': usuario})

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        libro = Libro.objects.get(pk=pk)
        usuario = self.request.user

        existe_Review = Review.objects.filter(libro=libro, usuario=usuario).first()

        if existe_Review:
            form = ReviewForm(request.POST, instance=existe_Review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.libro = libro
            review.usuario = usuario
            review.save()

            return redirect('list_books')

        return render(request, 'biblioteca_App/create_review.html', {'libro': libro, 'form': form, 'usuario': usuario})

# class CreateReview(View):
#     def get(self, request, pk):
#         libro = Libro.objects.get(pk=pk)
#         form = ReviewForm()
#         return render(request, 'biblioteca_App/create_review.html', {'form': form, 'libro':libro})
    
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             libro = Libro.objects.get(pk=pk)
#             Review.libro = libro
#             Review.usuario = self.request.user
#             form.save()
#             return redirect('review_book')
#         return render(request, 'biblioteca_App/create_review.html', {'form': form, 'libro':libro})


class DeleteReview(DeleteView):
    model = Review
    template_name = 'biblioteca_App/delete_review.html'
    success_url = reverse_lazy("list_books")


class PanelView(View):
    nombre_template = 'biblioteca_App/panel_bibliotecario.html'
    

    def get(self, request):
        NPrestamos = len(Prestamo.objects.filter(estado='prestado'))
        NDisponibles = len(Libro.objects.filter(disponibilidad='disponible'))

        fecha_actual = datetime.datetime.now()
        fecha_hace_15_dias = fecha_actual - datetime.timedelta(days=15)
        librosnodevueltos = Prestamo.objects.filter(estado='prestado', fecha_prestamo__lte=fecha_hace_15_dias)

        fecha_en_7_dias = fecha_actual + datetime.timedelta(days=7)
        librosadevolver = Prestamo.objects.filter(estado='prestado', fecha_devolucion__lte=fecha_en_7_dias, fecha_devolucion__gte=datetime.datetime.now())

        usuario = self.request.user

        return render(request, self.nombre_template, { 'librosadevolver': librosadevolver,'librosnodevueltos': librosnodevueltos,'ndisponibles': NDisponibles,'nprestamos': NPrestamos, 'usuario':usuario})
    