from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.


def home_dashbord(request):
    return render(request,"users/home_page.html",{})

# def login_view(request):
    
#     return render(request,"users/user_login.html",{})

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy("home")
    
def custom_logout_view(request):
    logout(request)
    return redirect('login')