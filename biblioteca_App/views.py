from .models import Libro
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
class ListBooks(ListView):
    model = Libro


class DetailBook(DetailView):
    model = Libro

class DeleteBook(DeleteView):
    model = Libro
    success_url = reverse_lazy("list_books")

class EditBook(UpdateView):
    model = Libro
    fields = ['titulo', 'autores','editorial','fecha_publicacion', 'genero','isbn','resumen', 'disponibilidad','portada']
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("list_books")

