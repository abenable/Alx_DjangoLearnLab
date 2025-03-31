from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
]