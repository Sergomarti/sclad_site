from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from django.views.generic import FormView

from ..forms import EmployeeSignUpForm, ProductForm, OrderResponseForm, ReturnResponseForm
from ..models import Product, User, Order, AdditionProduct, HistoryOrders


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
            return redirect('/home_employee/')
    else:
        form = ProductForm()

    return render(request, 'employee/add_product.html', {'form': form})


@login_required
@require_GET
def product_list_employee(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    products = Product.objects.filter(
        Q(brend__icontains=query) | Q(product__icontains=query)
    )
    pagin = Paginator(products, 2, orphans=1)
    return render(request, 'employee/product_list_employee.html', context={
        'page': pagin.page(page),

    })


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('/home_employee/')
    else:
        form = ProductForm(instance=product)
    return render(request, 'employee/edit_product.html',
                  {
                      'form': form
                  })


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return render(request, 'employee/delete_success.html')


@login_required
def edit_account_employee(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EmployeeSignUpForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            login(request, account)
            return redirect('/')
    else:
        form = EmployeeSignUpForm(instance=account)
    return render(request, 'employee/account_edit.html',
                  {
                      'form': form
                  })


@login_required
@require_GET
def order_list_employee(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    order = Order.objects.filter(Q(user__username__icontains=query) | Q(product__product__icontains=query),
                                 was_response=False)
    pagin = Paginator(order, 2, orphans=1)
    return render(request, 'employee/order_list.html',
                  {
                      'page': pagin.page(page)
                  })


@login_required
def order_response(request, pk):
    order = get_object_or_404(Order, pk=pk)
    pr = order.product
    number = pr.id
    product = get_object_or_404(Product, pk=number)
    if request.method == "POST":
        form = OrderResponseForm(request.POST)
        if form.is_valid():
            resp = form.save(commit=False)
            if resp.response.id == 1:
                order.was_response = True
                product.count -= order.count
                resp.order = order
                order.save()
                product.save()
                resp.save()
            else:
                order.was_response = True
                resp.order = order
                order.save()
                resp.save()
            return redirect('/order/')
    else:
        form = OrderResponseForm()
    return render(request, 'employee/order_response.html',
                  {
                      'form': form
                  })


@login_required
@require_GET
def return_list_employee(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    return_product = AdditionProduct.objects.filter(
        Q(user__username__icontains=query) | Q(product__product__icontains=query), was_response=False)
    pagin = Paginator(return_product, 2, orphans=1)
    return render(request, 'employee/return_list.html',
                  {
                      'page': pagin.page(page)
                  })


@login_required
def return_response(request, pk):
    return_product = get_object_or_404(AdditionProduct, pk=pk)
    pr = return_product.product
    number = pr.id
    product = get_object_or_404(Product, pk=number)
    if request.method == "POST":
        form = ReturnResponseForm(request.POST)
        if form.is_valid():
            resp = form.save(commit=False)
            if resp.response.id == 1:
                return_product.was_response = True
                product.count += return_product.count
                resp.addition = return_product
                return_product.save()
                product.save()
                resp.save()
            else:
                return_product.was_response = True
                resp.order = return_product
                return_product.save()
                resp.save()
            return redirect('/return/')
    else:
        form = ReturnResponseForm()
    return render(request, 'employee/return_response.html',
                  {
                      'form': form
                  })


@login_required
@require_GET
def order_response_list_employee(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    history = HistoryOrders.objects.filter(
        Q(response__response__icontains=query) | Q(order__product__brend__icontains=query),
        addition=None)
    pagin = Paginator(history, 2, orphans=1)
    return render(request, 'employee/history_response_order.html',
                  {
                      'page': pagin.page(page)
                  })


@login_required
@require_GET
def return_response_list_employee(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    history = HistoryOrders.objects.filter(
        Q(response__response__icontains=query) | Q(addition__product__brend__icontains=query), order=None)
    pagin = Paginator(history, 2, orphans=1)
    return render(request, 'employee/history_response_return.html',
                  {
                      'page': pagin.page(page)
                  })
