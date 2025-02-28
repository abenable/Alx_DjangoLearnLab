from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.crypto import get_random_string
from bookshelf.models import CustomUser

class ExtendedUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        # Password strength validation
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.profile.role = 'MEMBER'  # Default role for new users
            user.profile.save()
        return user

@require_http_methods(["GET", "POST"])
@sensitive_post_parameters('password1', 'password2')
def register(request):
    if request.user.is_authenticated:
        return redirect('bookshelf:member_dashboard')
        
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('bookshelf:member_dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred during registration.')
                return redirect('bookshelf:register')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'relationship_app/auth/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
@sensitive_post_parameters('password')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('bookshelf:member_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Login successful.')
                
                # Redirect based on role
                if user.profile.role == 'ADMIN':
                    return redirect('bookshelf:admin_dashboard')
                elif user.profile.role == 'LIBRARIAN':
                    return redirect('bookshelf:librarian_dashboard')
                else:
                    return redirect('bookshelf:member_dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred during login.')
                return redirect('bookshelf:login')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    except Exception as e:
        messages.error(request, 'An error occurred during logout.')
    return redirect('bookshelf:login')

@login_required
@sensitive_post_parameters('old_password', 'new_password1', 'new_password2')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('bookshelf:member_dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while changing your password.')
                return redirect('bookshelf:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'relationship_app/auth/change_password.html', {'form': form})