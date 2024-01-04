from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import Product, CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    storeName = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'storeName', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'  # Bootstrap form layout
        self.helper.label_class = 'col-lg-2'  # Bootstrap column size for labels
        self.helper.field_class = 'col-lg-10'  # Bootstrap column size for form fields
        self.helper.layout = Layout(
            Field('name', css_class='form-control', placeholder='Enter product name'),
            Field('price', css_class='form-control', placeholder='Enter product price'),
            Field('description', css_class='form-control', placeholder='Enter product description'),
            Field('image', css_class='form-control', placeholder='Enter product image URL'),
            'user',  # Hidden field
            Submit('submit', 'Save product', css_class='btn btn-success')
        )

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 4:
            raise forms.ValidationError("Name must be at least 4 characters.")
        elif data[0] == ' ':
            raise forms.ValidationError("No space at the beginning of name and it must be at least 4 characters.")
        return data

    def clean_price(self):
        data = self.cleaned_data['price']
        if data <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return data
    
    def clean_description(self):
        data = self.cleaned_data['description']
        if len(data) < 10:
            raise forms.ValidationError("product description must be at least 3 characters.")
        elif data[0] == ' ':
            raise forms.ValidationError("No space at the beginning of description and it must be at least 3 characters.")
        return data
