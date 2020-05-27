from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, FormView)

from ..decorators import employee_required
from ..forms import EmployeeSignUpForm, ClientSignUpForm, ProductForm
from ..models import Product, User


def home_employee(request):
    return render(request, 'home_employee.html')


class EmployeeSignUpView(FormView):
    form_class = EmployeeSignUpForm
    initial = {'key': 'value'}
    template_name = 'registration/signup_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.send_verification_email()
            login(request, user)
            return render(request, 'registration/signup_success.html')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('home_client/')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def product_list_employee(request):
    products = Product.object.filter(type_of_goods=User.type_of_goods)
    return render(request, 'product_list_employee.html',
                  {
                      'products': products
                  })