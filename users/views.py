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


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, StudentProfileForm, InstructorProfileForm
from .models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            if request.POST.get('user_type') == 'instructor':
                user.is_instructor = True
                user.is_student = False
                user.save()
                
                profile_form = InstructorProfileForm(request.POST)
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
            else:
                profile_form = StudentProfileForm(request.POST)
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
            
            login(request, user)
            return redirect('home')  # আপনার হোমপেজের URL দিয়ে পরিবর্তন করুন
            
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'student_form': StudentProfileForm(),
        'instructor_form': InstructorProfileForm()
    })
    
    
    
    
    

def terms_of_service(request):
    return render(request, 'legal/terms.html', {'title': 'Terms of Service'})