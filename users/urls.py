from django.urls import path

from .views import main, client, employee

urlpatterns = [
    path('', main.home, name='home'),
    path('home_client/', client.product_list_client, name='home_client'),
    path('account/<int:pk>/edit_account_client/', client.edit_account_client, name='edit_account_client'),

    path('product/<int:pk>/order_product/', client.order_product, name='order_product'),
    path('order_success/', client.order_success, name='order_success'),
    path('history_ord_client/', client.order_response_list_client, name='history_order_response_client'),

    path('product/<int:pk>/return/', client.return_product, name='return_product'),
    path('return_success/', client.return_success, name='return_success'),
    path('history_ret_client/', client.return_response_list_client, name='history_return_response_client'),

    path('home_employee/', employee.product_list_employee, name='home_employee'),
    path('add_product/', employee.add_product, name='add_product'),
    path('product/<int:pk>/edit_product/', employee.edit_product, name='edit_product'),
    path('product/<int:pk>/delete_product/', employee.delete_product, name='delete_product'),
    path('account/<int:pk>/edit_account_employee/', employee.edit_account_employee, name='edit_account_employee'),

    path('order/', employee.order_list_employee, name='order'),
    path('order/<int:pk>/order_response/', employee.order_response, name='order_response'),
    path('history_ord_employee/', employee.order_response_list_employee, name='history_order_response_employee'),

    path('return/', employee.return_list_employee, name='return'),
    path('return/<int:pk>/return_response/', employee.return_response, name='return_response'),
    path('history_ret_employee/', employee.return_response_list_employee, name='history_return_response_employee'),
]
