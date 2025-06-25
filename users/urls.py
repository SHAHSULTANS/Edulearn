
from django.urls import include, path

from users import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
   path('login/', views.UserLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
    
]
