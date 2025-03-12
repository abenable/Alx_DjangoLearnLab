from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class BookListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating books.
    
    GET: Returns a list of all books
    POST: Creates a new book
    
    Filtering:
    - Filter by title: ?title=example
    - Filter by publication_year: ?publication_year=2023
    - Filter by author's id: ?author=1
    
    Searching:
    - Search in title: ?search=example
    
    Ordering:
    - Order by title: ?ordering=title
    - Order by publication_year (ascending): ?ordering=publication_year
    - Order by publication_year (descending): ?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year']


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific book.
    
    GET: Returns details of a specific book
    PUT/PATCH: Updates a specific book
    DELETE: Deletes a specific book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating authors.
    
    GET: Returns a list of all authors, including their books
    POST: Creates a new author
    
    Filtering:
    - Filter by name: ?name=example
    
    Searching:
    - Search in name: ?search=example
    
    Ordering:
    - Order by name: ?ordering=name
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific author.
    
    GET: Returns details of a specific author, including their books
    PUT/PATCH: Updates a specific author
    DELETE: Deletes a specific author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
