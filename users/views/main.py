from django.core.exceptions import NON_FIELD_ERRORS
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

from users.forms import LoginForm


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_employee:
            return redirect('/home_employee/')
        else:
            return redirect('/home_client/')
    return render(request, 'home.html')


def verify(request):
    user = request.user
    data = request.GET
    if user.is_token_correct(data['token']):
        user.verify_email()
        return render(request, 'registration/email_verified.html')
    else:
        return Http404("Not Found")


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'registration/login.html', context={
            'form': form
        })
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        form.is_valid()
        user = form.get_user(request)
        # and user.is_email_verified:
        if user:
            login(request, user)
            if user.is_client:
                return redirect('/home_client/')
            else:
                return redirect('/home_employee/')
        else:
            form.errors[NON_FIELD_ERRORS] = [
                'Cannot perform login with this credentials'
            ]
            return render(request, 'registration/login.html', context={
                "form": form
            })


def logout_user(request):
    logout(request)
    return redirect("/")
