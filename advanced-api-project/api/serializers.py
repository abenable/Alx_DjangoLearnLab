from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion of Book model instances into JSON representation,
    and includes custom validation for the publication_year field to ensure it's not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication_year is not in the future.
        
        Args:
            value: The publication year to validate
            
        Returns:
            The validated year if valid
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future. Current year is {current_year}.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    This serializer includes a nested BookSerializer to represent all books written by an author,
    demonstrating the handling of nested relationships in Django REST Framework.
    """
    # Nested serialization of all books by this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']