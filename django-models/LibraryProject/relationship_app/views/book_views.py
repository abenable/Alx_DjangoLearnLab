from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Book, Library

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