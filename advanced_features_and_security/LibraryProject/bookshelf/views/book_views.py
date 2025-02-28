from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.utils.html import escape
from bookshelf.models import Book, Library
from django import forms

class BookForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Remove any potential script tags or dangerous content
            title = escape(title.strip())
            # Validate length
            if len(title) < 1 or len(title) > 200:
                raise ValidationError('Title must be between 1 and 200 characters.')
        return title

    class Meta:
        model = Book
        fields = ['title', 'author']

@login_required
def book_list(request):
    try:
        books = Book.objects.all().select_related('author')
        context = {
            'books': books,
            'user_role': request.user.profile.role,
            'can_add': request.user.has_perm('bookshelf.can_add_book'),
            'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
            'can_delete': request.user.has_perm('bookshelf.can_delete_book')
        }
        return render(request, 'relationship_app/book/book_list.html', context)
    except Exception as e:
        messages.error(request, 'An error occurred while fetching the book list.')
        return redirect('bookshelf:member_dashboard')

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_add_book'
    raise_exception = True

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to add books.")
        return redirect('bookshelf:book_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book created successfully.')
            return response
        except Exception as e:
            messages.error(self.request, 'Error creating book.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context['user_role'] = self.request.user.profile.role
        return context

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_edit_book'
    raise_exception = True

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit books.")
        return redirect('bookshelf:book_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book updated successfully.')
            return response
        except Exception as e:
            messages.error(self.request, 'Error updating book.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['user_role'] = self.request.user.profile.role
        return context

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'relationship_app/book/book_confirm_delete.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_delete_book'
    raise_exception = True

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete books.")
        return redirect('bookshelf:book_list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Book deleted successfully.')
            return response
        except Exception as e:
            messages.error(request, 'Error deleting book.')
            return redirect('bookshelf:book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role
        return context

@permission_required('bookshelf.can_view_book_details', raise_exception=True)
def book_detail(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk)
        context = {
            'book': book,
            'user_role': request.user.profile.role,
            'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
            'can_delete': request.user.has_perm('bookshelf.can_delete_book')
        }
        return render(request, 'relationship_app/book/book_detail.html', context)
    except Exception as e:
        messages.error(request, 'Error retrieving book details.')
        return redirect('bookshelf:book_list')

class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    raise_exception = True

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['user_role'] = self.request.user.profile.role
            return context
        except Exception as e:
            messages.error(self.request, 'Error retrieving library details.')
            return {}