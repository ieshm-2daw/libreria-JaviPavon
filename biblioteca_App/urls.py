from django.urls import path
from .views import ListBooks, DetailBook, DeleteBook, EditBook

urlpatterns = [
    path('', ListBooks.as_view(), name='list_books'),
    path('detail/<int:pk>', DetailBook.as_view(), name='detail_book'),
    path('delete/<int:pk>', DeleteBook.as_view(), name='delete_book'),
    path('edit/<int:pk>', EditBook.as_view(), name='edit_book'),

]