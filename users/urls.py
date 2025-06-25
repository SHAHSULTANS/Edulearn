
from django.urls import include, path

from users import views



urlpatterns = [
   path('login/', views.UserLoginView.as_view(), name='login'),
    
]
