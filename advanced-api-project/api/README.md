# Advanced API Project Documentation

## API Endpoints

### Books

#### List and Create Books

- **URL:** `/api/books/`
- **Methods:**
  - `GET`: List all books
  - `POST`: Create a new book (Authentication required)
- **Filtering Options:**
  - Filter by title: `?title=example`
  - Filter by publication year: `?publication_year=2023`
  - Filter by author: `?author=1`
- **Search:**
  - Search in title: `?search=example`
- **Ordering:**
  - Order by title: `?ordering=title`
  - Order by publication year: `?ordering=publication_year` or `?ordering=-publication_year`

#### Single Book Operations

- **URL:** `/api/books/<id>/`
- **Methods:**
  - `GET`: Retrieve book details
  - `PUT/PATCH`: Update book (Authentication required)
  - `DELETE`: Delete book (Authentication required)

### Authors

#### List and Create Authors

- **URL:** `/api/authors/`
- **Methods:**
  - `GET`: List all authors
  - `POST`: Create a new author (Authentication required)
- **Filtering Options:**
  - Filter by name: `?name=example`
- **Search:**
  - Search in name: `?search=example`
- **Ordering:**
  - Order by name: `?ordering=name`

#### Single Author Operations

- **URL:** `/api/authors/<id>/`
- **Methods:**
  - `GET`: Retrieve author details
  - `PUT/PATCH`: Update author (Authentication required)
  - `DELETE`: Delete author (Authentication required)

## Authentication

The API uses Django REST Framework's built-in authentication. For protected endpoints (POST, PUT, PATCH, DELETE):

- Include authentication credentials in your request
- Unauthenticated users can only perform read operations (GET)

## Example Usage

### List all books

```bash
curl http://localhost:8000/api/books/
```

### Create a new book (authenticated)

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title":"New Book","publication_year":2024,"author":1}'
```

### Filter books by publication year

```bash
curl http://localhost:8000/api/books/?publication_year=2024
```

### Search books

```bash
curl http://localhost:8000/api/books/?search=django
```
