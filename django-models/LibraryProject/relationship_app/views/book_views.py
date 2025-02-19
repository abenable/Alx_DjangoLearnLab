from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from relationship_app.models import Book, Library
from django import forms

@login_required
def book_list(request):
    books = Book.objects.all().select_related('author')
    context = {
        'books': books,
        'user_role': request.user.profile.role
    }
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role
        return context

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book/book_form.html'
    success_url = reverse_lazy('relationship_app:book_list')
    permission_required = 'relationship_app.can_add_book'

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to add books.")
        return redirect('relationship_app:book_list')

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book/book_form.html'
    success_url = reverse_lazy('relationship_app:book_list')
    permission_required = 'relationship_app.can_change_book'  # Updated from can_edit_book to match model permission

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit books.")
        return redirect('relationship_app:book_list')

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'relationship_app/book/book_confirm_delete.html'
    success_url = reverse_lazy('relationship_app:book_list')
    permission_required = 'relationship_app.can_delete_book'

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete books.")
        return redirect('relationship_app:book_list')

@permission_required('relationship_app.can_view_book_details', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/book/book_detail.html', {'book': book})