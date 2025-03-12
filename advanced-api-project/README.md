# Advanced API Project with Django REST Framework

This project demonstrates advanced API development using Django REST Framework, focusing on custom serializers, filtering, searching, and ordering capabilities.

## Project Structure

- `api/models.py`: Contains Author and Book models with a one-to-many relationship
- `api/serializers.py`: Custom serializers for handling nested relationships and validation
- `api/views.py`: API views with filtering, searching, and ordering capabilities
- `api/test_views.py`: Comprehensive unit tests for API endpoints

## Features

1. **Custom Serializers**

   - Nested relationships between Author and Book models
   - Custom validation for publication year

2. **Generic Views**

   - List, create, retrieve, update, and delete operations
   - Permission controls based on authentication

3. **Filtering, Searching, Ordering**

   - Filter books by title, publication year, and author
   - Search books by title
   - Order books by title or publication year

4. **Comprehensive Testing**
   - Unit tests for CRUD operations
   - Tests for permission controls
   - Tests for filtering, searching, and ordering capabilities

## API Endpoints

- `/api/books/` - List all books or create a new book
- `/api/books/{id}/` - Retrieve, update, or delete a specific book
- `/api/authors/` - List all authors or create a new author
- `/api/authors/{id}/` - Retrieve, update, or delete a specific author

## Query Parameters

### Books

- `?title=...` - Filter books by title
- `?publication_year=...` - Filter books by year
- `?author=...` - Filter books by author ID
- `?search=...` - Search books by title
- `?ordering=title` or `?ordering=publication_year` - Order results

### Authors

- `?name=...` - Filter authors by name
- `?search=...` - Search authors by name
- `?ordering=name` - Order results by name

## Running Tests

```bash
python manage.py test api
```

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
