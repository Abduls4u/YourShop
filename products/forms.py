from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from products.models import Product

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']
        widgets = {'user': forms.HiddenInput()}