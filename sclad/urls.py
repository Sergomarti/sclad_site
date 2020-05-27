"""sclad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from users.views import main, client, employee

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('signup/', main.SignUpView.as_view(), name='signup'),
    path('logout/', main.logout_user, name='logout'),
    path('login/', main.login_user, name='login'),
    path('verify/', main.verify, name='verify'),
    path('signup/student/', client.ClientSignUpView.as_view(), name='client_signup'),
    path('signup/teacher/', employee.EmployeeSignUpView.as_view(), name='employee_signup'),
    path('', include('users.urls')),
]
