from django.urls import path
from .views import ListBooks, DetailBook

urlpatterns = [
    path('', ListBooks.as_view(), name='list_books'),
    path('detail/<int:pk>', DetailBook.as_view(), name='detail_book'),

]