from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """Test case for Book API endpoints"""

    def setUp(self):
        """Set up test data"""
        # Create a user for authentication tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='John Doe')
        self.author2 = Author.objects.create(name='Jane Smith')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Test Book 2',
            publication_year=2021,
            author=self.author2
        )
        
        # URLs for the tests
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book1.id])
        self.author_list_url = reverse('author-list')
        self.author_detail_url = reverse('author-detail', args=[self.author1.id])

    def test_get_book_list(self):
        """Test retrieving a list of books"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_book_detail(self):
        """Test retrieving a single book"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')

    def test_create_book_authenticated(self):
        """Test creating a book when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='New Test Book').publication_year, 2023)

    def test_create_book_unauthenticated(self):
        """Test creating a book when unauthenticated (should fail)"""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No new book should be created

    def test_update_book_authenticated(self):
        """Test updating a book when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2022,
            'author': self.author2.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
        self.assertEqual(self.book1.author, self.author2)

    def test_delete_book_authenticated(self):
        """Test deleting a book when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        response = self.client.get(f"{self.book_list_url}?title=Test Book 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')

    def test_filter_books_by_year(self):
        """Test filtering books by publication year"""
        response = self.client.get(f"{self.book_list_url}?publication_year=2021")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 2')

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get(f"{self.book_list_url}?search=Book 2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 2')

    def test_order_books_by_year(self):
        """Test ordering books by publication year"""
        response = self.client.get(f"{self.book_list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')  # 2020 comes before 2021

    def test_invalid_book_data(self):
        """Test validation for future publication year"""
        self.client.login(username='testuser', password='testpass123')
        next_year = timezone.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': next_year,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the validation error message is in the response
        self.assertIn('publication_year', response.data)


class AuthorAPITestCase(APITestCase):
    """Test case for Author API endpoints"""

    def setUp(self):
        """Set up test data"""
        # Create a user for authentication tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='John Doe')
        self.author2 = Author.objects.create(name='Jane Smith')
        
        # Create test books for the authors
        self.book1 = Book.objects.create(
            title='John Book 1',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='John Book 2',
            publication_year=2021,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Jane Book',
            publication_year=2022,
            author=self.author2
        )
        
        # URLs for the tests
        self.author_list_url = reverse('author-list')
        self.author_detail_url = reverse('author-detail', args=[self.author1.id])

    def test_get_author_list(self):
        """Test retrieving a list of authors"""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_author_detail(self):
        """Test retrieving a single author with their books"""
        response = self.client.get(self.author_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(len(response.data['books']), 2)  # Author 1 has 2 books

    def test_create_author_authenticated(self):
        """Test creating an author when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        data = {'name': 'New Test Author'}
        response = self.client.post(self.author_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 3)
        self.assertEqual(Author.objects.get(name='New Test Author').name, 'New Test Author')

    def test_filter_authors_by_name(self):
        """Test filtering authors by name"""
        response = self.client.get(f"{self.author_list_url}?name=Jane Smith")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Jane Smith')