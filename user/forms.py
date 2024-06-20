from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerSignUpForm(UserCreationForm, forms.Form):
    username = forms.EmailField(required=True, label='Login Email')
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    company = forms.CharField(max_length=255)
    contact = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.EmailField(required=False, label='Login Email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not username:
            self.add_error('username', 'You must provide a username')
        if not first_name:
            self.add_error('first_name', 'This field is required.')
        if not last_name:
            self.add_error('last_name', 'This field is required.')


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'company', 'contact']

        labels = {
            'email': 'Company Email',
        }
