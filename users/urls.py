from django.urls import path, include

from . import views
from .views import main, client, employee
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main.home, name='home'),
    path('home_client/', client.product_list_client, name='home_client'),
    path('product/<int:pk>/order_product/', client.order_product, name='order_product'),
    path('order_success/', client.order_success, name='order_success'),
    path('product/<int:pk>/return/', employee.edit_product, name='return_product'),
    path('return_success/', client.return_success, name='return_success'),

    path('home_employee/', employee.product_list_employee, name='home_employee'),
    path('add_product/', employee.add_product, name='add_product'),
    path('product/<int:pk>/edit_product/', employee.edit_product, name='edit_product'),

]
