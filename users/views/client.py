import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from django.views.generic import FormView

from ..forms import ClientSignUpForm, OrderForm, ReturnForm
from ..models import Product, User, TypeOfGoods, HistoryOrders, Order


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


def edit_account_client(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ClientSignUpForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            login(request, account)
            return redirect('/')
    else:
        form = ClientSignUpForm(instance=account)
    return render(request, 'client/account_edit.html',
                  {
                      'form': form
                  })


@login_required
@require_GET
def product_list_client(request):
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    user = request.user
    type_of_goods_client = user.type_of_goods
    type_of_good = type_of_goods_client.id
    if type_of_good == 1:
        products = Product.objects.filter(
            Q(brend__icontains=query) | Q(product__icontains=query)
        )
    else:
        products = Product.objects.filter(Q(brend__icontains=query) | Q(product__icontains=query))
        products = products.filter(type_of_goods=user.type_of_goods)
    pagin = Paginator(products, 2, orphans=1)
    return render(request, 'client/product_list_client.html',
                  {
                      'page': pagin.page(page)
                  })


@login_required
def order_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.date = datetime.datetime.now().date()
            order.product = product
            order.save()
            return redirect('/order_success/')
    else:
        form = OrderForm()
    return render(request, 'client/order_product.html',
                  {
                      'form': form
                  })


@login_required
def order_success(request):
    return render(request, 'client/order_success.html')


@login_required
def return_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_pr = form.save(commit=False)
            return_pr.user = request.user
            return_pr.product = product
            return_pr.save()
            return redirect('/return_success/')
    else:
        form = ReturnForm()
    return render(request, 'client/return_product.html',
                  {
                      'form': form
                  })


@login_required
def return_success(request):
    return render(request, 'client/return_success.html')


@login_required
@require_GET
def order_response_list_client(request):
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    user = request.user
    history = HistoryOrders.objects.filter(
        Q(response__response__icontains=query) | Q(order__product__brend__icontains=query), addition=None,
        order__user=user)
    pagin = Paginator(history, 2, orphans=1)
    return render(request, 'client/history_response_order.html',
                  {
                      'page': pagin.page(page)
                  })


@login_required
@require_GET
def return_response_list_client(request):
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    user = request.user
    history = HistoryOrders.objects.filter(
        Q(response__response__icontains=query) | Q(addition__product__brend__icontains=query), order=None,
        addition__user=user)
    pagin = Paginator(history, 2, orphans=1)
    return render(request, 'client/history_response_return.html',
                  {
                      'page': pagin.page(page)
                  })
