from django.db import models
from django.utils import timezone

class Author(models.Model):
    """
    Author model representing a book author in the library system.
    
    This model stores basic information about authors, and has a one-to-many
    relationship with the Book model (one author can write many books).
    """
    name = models.CharField(max_length=100, help_text="Name of the author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model representing a book in the library system.
    
    This model stores information about books, including the title, publication year,
    and a foreign key reference to the author. The relationship with Author is 
    many-to-one (many books can be written by one author).
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author who wrote this book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
