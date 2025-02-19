from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Set up initial permissions for different user roles'

    def handle(self, *args, **kwargs):
        # Get or create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        librarian_group, _ = Group.objects.get_or_create(name='Librarian')
        member_group, _ = Group.objects.get_or_create(name='Member')

        # Get content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all book permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)

        # Set up admin permissions (all permissions)
        admin_group.permissions.set(book_permissions)

        # Set up librarian permissions
        librarian_permissions = book_permissions.filter(codename__in=[
            'can_add_book',
            'can_edit_book',
            'can_view_book_details'
        ])
        librarian_group.permissions.set(librarian_permissions)

        # Set up member permissions
        member_permissions = book_permissions.filter(codename__in=[
            'can_view_book_details'
        ])
        member_group.permissions.set(member_permissions)

        # Assign users to groups based on their role
        for user in User.objects.all():
            try:
                role = user.profile.role
                if role == 'ADMIN':
                    admin_group.user_set.add(user)
                elif role == 'LIBRARIAN':
                    librarian_group.user_set.add(user)
                elif role == 'MEMBER':
                    member_group.user_set.add(user)
            except UserProfile.DoesNotExist:
                continue

        self.stdout.write(self.style.SUCCESS('Successfully set up permissions'))