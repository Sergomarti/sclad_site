from django.contrib.auth import authenticate
from django import forms

from django.contrib.auth.hashers import make_password
from django.forms import ModelForm

from users.models import User, Product, Order, AdditionProduct, HistoryOrders


class EmployeeSignUpForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'telephone',
            'type_of_goods',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.cleaned_data['password'])
        user = super().save(self)
        user.is_employee = True
        return user

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("Password don't math")

        return self.cleaned_data

    def clean_username(self):
        username = self.data['username']
        if not username.isalpha():
            raise forms.ValidationError("Username containts forbidden characters")

        return username

    def clean_telephone(self):
        telephone = self.data['telephone']
        if telephone.isalpha():
            raise forms.ValidationError("Telephone should contains ONLY digits")

        return telephone


class ClientSignUpForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'telephone',
            'type_of_goods',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.cleaned_data['password'])
        user = super().save(self)
        user.is_client = True
        return user

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("Password don't math")

        return self.cleaned_data

    def clean_username(self):
        username = self.data['username']
        if not username.isalpha():
            raise forms.ValidationError("Username containts forbidden characters")

        return username

    def clean_telephone(self):
        telephone = self.data['telephone']
        if telephone.isalpha():
            raise forms.ValidationError("Telephone should contains ONLY digits")

        return telephone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def get_user(self, request):
        return authenticate(
            request,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brend', 'product', 'count', 'type_of_goods', 'image']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['count', 'comment']


class ReturnForm(ModelForm):
    class Meta:
        model = AdditionProduct
        fields = ['count', 'comment']


class OrderResponseForm(ModelForm):
    class Meta:
        model = HistoryOrders
        fields = ['response', 'comment']


class ReturnResponseForm(ModelForm):
    class Meta:
        model = HistoryOrders
        fields = ['response', 'comment']
