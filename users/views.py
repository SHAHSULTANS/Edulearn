from django.shortcuts import redirect, render

from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


def home_dashbord(request):
    return render(request,"users/home_page.html",{})

# def login_view(request):
    
#     return render(request,"users/user_login.html",{})

class UserLoginView(LoginView):
    template_name = 'users/login.html'