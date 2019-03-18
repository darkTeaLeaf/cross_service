from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False)
    telegram_alias = forms.IntegerField(required=True)

    class Meta:
        fields = [
            'username', 'first_name', 'last_name', 'email', 'telegram_alias'
        ]
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        # telegram_alias = self.cleaned_data['telegram_alias']
        if commit:
            user.save(True)