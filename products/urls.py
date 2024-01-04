from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register', views.register, name='register'),
    path('manage_products', views.manage_products, name='manage_products'),
    path('<int:user_id>/storefront', views.storefront, name='storefront'),
    path('', views.about, name='about'),
    path('login', LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]