from django.urls import path
from .views import (
    ListBooks, 
    DetailBook,
    DeleteBook, 
    EditBook, 
    FormBooks, 
    PrestamoBook, 
    CancelarPrestamo, 
    ListMyBooks, 
    ReviewBook, 
    CreateReview, 
    DeleteReview,
    PanelView
    )

urlpatterns = [
    path('', ListBooks.as_view(), name='list_books'),
    path('detail/<int:pk>', DetailBook.as_view(), name='detail_book'),
    path('delete/<int:pk>', DeleteBook.as_view(), name='delete_book'),
    path('edit/<int:pk>', EditBook.as_view(), name='edit_book'),
    path('createbook', FormBooks.as_view(), name='create_book'),
    path('pedido/<int:pk>', PrestamoBook.as_view(), name='pedido_book'),
    path('cancelar/pedido/<int:pk>', CancelarPrestamo.as_view(), name='cancel_pedido'),
    path('mybooks', ListMyBooks.as_view(), name='list_my_books'),
    path('reviewbook/<int:pk>', ReviewBook.as_view(), name='review_book'),
    path('createreview/<int:pk>', CreateReview.as_view(), name='create_review'),
    path('deletereview/<int:pk>', DeleteReview.as_view(), name='delete_review'),
    path('panel', PanelView.as_view(), name='panel'),
]