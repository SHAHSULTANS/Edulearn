
from django.urls import include, path

from users import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
   path('login/', views.UserLoginView.as_view(), name='login'),
   path('logout/', views.custom_logout_view, name='logout'),
   path('register/', views.register, name='register'),
   path('terms/', views.terms_of_service, name='terms_of_service'),
    
]
