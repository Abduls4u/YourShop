from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register', views.register, name='register'),
    path('manage_products', views.manage_products, name='manage_products'),
    path('<int:user_id>/view_user_products', views.view_user_products, name='view_user_products'),
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]