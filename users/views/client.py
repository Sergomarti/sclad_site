from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, FormView

from ..forms import ClientSignUpForm
from ..models import Product, User


def home_client(request):
    return render(request, 'home_client.html')


class ClientSignUpView(FormView):
    form_class = ClientSignUpForm
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


def product_list_client(request):
    user = request.user
    products = Product.objects.filter(type_of_goods=user.type_of_goods)
    return render(request, 'product_list_client.html',
                  {
                      'products': products
                  })
