from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'books-viewset', BookViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
]