from django.urls import path, include

from . import views
from .views import main, client, employee
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main.home, name='home'),
    path('home_client/', client.home_client, name='home_client'),
    path('product_list_client/', client.product_list_client, name='product_list_client'),

    path('home_employee/', employee.product_list_employee, name='home_employee'),
    path('add_product/', employee.add_product, name='add_product'),
    path('product/<int:pk>/edit_product/', employee.edit_product, name='edit_product'),

]
