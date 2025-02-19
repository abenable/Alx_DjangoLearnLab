from relationship_app.views.admin_view import admin_view
from relationship_app.views.librarian_view import librarian_view
from relationship_app.views.member_view import member_view
from relationship_app.views.book_views import book_list, LibraryDetailView
from relationship_app.views.auth_views import register

__all__ = [
    'admin_view', 
    'librarian_view', 
    'member_view',
    'book_list',
    'LibraryDetailView',
    'register'
]