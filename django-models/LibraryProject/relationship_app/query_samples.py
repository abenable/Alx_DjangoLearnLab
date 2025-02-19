from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    # Query all books by a specific author using filter
    return Book.objects.filter(author=author)

def list_library_books(library_name):
    # List all books in a library using filter
    return Book.objects.filter(libraries__name=library_name)

def get_library_librarian(library_name):
    # Retrieve the librarian for a library
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except Library.DoesNotExist:
        return None
