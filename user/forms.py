from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Feedback
from .models import USER_PROFILE_DATA

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ('feedback', 'grade', 'type')


# class CreateUserForm(UserCreationForm):
#     email = forms.EmailField(required=False)
#     telegram_alias = forms.IntegerField(required=True)
#
#     class Meta:
#         fields = [
#             'username', 'first_name', 'last_name', 'email', 'alias'
#         ]
#         model = User
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         # telegram_alias = self.cleaned_data['telegram_alias']
#         if commit:
#             user.save(True)


# class EditUserForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#     alias = forms.CharField(required=False)
#     # bio = forms.Textarea()
#
#     class Meta:
#         fields = [
#             'username', 'first_name', 'last_name', 'email', 'password', 'alias',
#         ]
#         model = User
#
#     def clean_email(self):
#         username = self.cleaned_data.get('username')
#         email = self.cleaned_data.get('email')
#
#         if email and User.objects.filter(email=email).exclude(username=username).count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#
#         if commit:
#             user.save()
#
#         # return user