from .models import Libro


from django.views.generic import (
    ListView,
    DetailView,
)
class ListBooks(ListView):
    model = Libro


class DetailBook(DetailView):
    model = Libro
