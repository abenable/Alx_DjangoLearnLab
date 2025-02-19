from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Book and Library paths
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication paths
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/auth/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based view paths
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_view, name='member_dashboard'),
]