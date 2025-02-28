from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from bookshelf.models import Library, Book

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'LIBRARIAN'

@user_passes_test(is_librarian)
def librarian_view(request):
    libraries = Library.objects.prefetch_related('books', 'books__author').all()
    context = {
        'libraries': libraries,
        'title': 'Library Management',
        'role': 'Librarian'
    }
    return render(request, 'relationship_app/role_views/librarian_view.html', context)

@login_required
@permission_required('bookshelf.can_view_library', raise_exception=True)
def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'library/library_list.html', {'libraries': libraries})

@login_required
@permission_required('bookshelf.can_create_library', raise_exception=True)
def create_library(request):
    if request.method == 'POST':
        # Add library creation logic here
        pass
    return render(request, 'library/create_library.html')

@login_required
@permission_required('bookshelf.can_edit_library', raise_exception=True)
def edit_library(request, library_id):
    library = get_object_or_404(Library, pk=library_id)
    if request.method == 'POST':
        # Add library editing logic here
        pass
    return render(request, 'library/edit_library.html', {'library': library})

@login_required
@permission_required('bookshelf.can_delete_library', raise_exception=True)
def delete_library(request, library_id):
    library = get_object_or_404(Library, pk=library_id)
    if request.method == 'POST':
        library.delete()
        return redirect('library_list')
    return render(request, 'library/delete_library.html', {'library': library})

@login_required
@permission_required('bookshelf.can_manage_books', raise_exception=True)
def manage_library_books(request, library_id):
    library = get_object_or_404(Library, pk=library_id)
    if request.method == 'POST':
        # Add book management logic here
        pass
    return render(request, 'library/manage_books.html', {'library': library})