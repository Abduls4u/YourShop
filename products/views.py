from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm, RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return (redirect(reverse('manage_products')))
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'products/register.html', context)

@login_required(login_url='login')
def manage_products(request):
    user_products = Product.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return (redirect(reverse('manage_products')))
    else:
            form = ProductForm()
    context = {
        'user_name': request.user.username,
        'user_products': user_products,
        'form': form,
        'user_id': request.user.id,
    }
    return (render(request, 'products/manage_products.html', context))

def view_user_products(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_products = Product.objects.filter(user=user)
    context = {
        'user': user,
        'user_products': user_products
    }
    return (render(request, 'products/view_user_products.html', context))

def index(request):
    context = {}
    return (render(request, 'products/layout.html', context))

