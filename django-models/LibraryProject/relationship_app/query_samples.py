from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    # Query all books by a specific author
    author = Author.objects.get(name=author_name)
    return author.books.all()

def list_library_books(library_name):
    # List all books in a library
    library = Library.objects.get(name=library_name)
    return library.books.all()

def get_library_librarian(library_name):
    # Retrieve the librarian for a library
    library = Library.objects.get(name=library_name)
    return library.librarian

# Example usage:
"""
# Create sample data
author = Author.objects.create(name="J.K. Rowling")
book = Book.objects.create(title="Harry Potter", author=author)
library = Library.objects.create(name="City Library")
library.books.add(book)
librarian = Librarian.objects.create(name="John Doe", library=library)

# Run queries
books = query_books_by_author("J.K. Rowling")
library_books = list_library_books("City Library")
librarian = get_library_librarian("City Library")
"""