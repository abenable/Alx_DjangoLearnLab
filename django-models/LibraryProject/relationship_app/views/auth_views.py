from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class ExtendedUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.profile.role = 'MEMBER'  # Default role for new users
            user.profile.save()
        return user

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:member_dashboard')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'relationship_app/auth/register.html', {'form': form})