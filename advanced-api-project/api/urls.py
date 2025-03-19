from django.urls import path
from .views import (
    BookListCreateView, BookDetailView, 
    AuthorListCreateView, AuthorDetailView,
    CreateView, UpdateView, DeleteView
)

app_name = 'api'

urlpatterns = [
    # Book URLs
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/update/', UpdateView.as_view(), name='book-update'),
    path('books/delete/', DeleteView.as_view(), name='book-delete'),
    ]