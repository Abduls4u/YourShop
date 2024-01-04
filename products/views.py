from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product, CustomUser
from .forms import ProductForm, RegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    form = ProductForm()
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'add_product':
            # Handle product creation
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect(reverse('manage_products'))

        elif action == 'delete_product':
            # Handle product deletion
            product_id = request.POST.get('delete_product_id', None)
            if product_id:
                product = get_object_or_404(Product, id=product_id, user=request.user)
                product.delete()
                return redirect(reverse('manage_products'))

    # Retrieve and display existing products
    products = Product.objects.filter(user=request.user)
    storeRelUrl = reverse('storefront', args=[request.user.id])
    storeAbsUrl = request.build_absolute_uri(storeRelUrl)
    context = {
        'user_name': request.user.username,
        'form': form,
        'products': products,
        'storeLink': storeAbsUrl,
    }
    return render(request, 'products/manage_products.html', context)

def storefront(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_products = Product.objects.filter(user=user).order_by('id')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(user_products, 9)
    try:
        user_products_paginated = paginator.page(page)
    except PageNotAnInteger:
        user_products_paginated = paginator.page(1)
    except EmptyPage:
        user_products_paginated = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'user_products': user_products_paginated,
        'valid_user': request.user,
    }
    return render(request, 'products/storefront.html', context)


def about(request):
    context = {}
    return (render(request, 'products/about.html', context))
