
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')

    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

