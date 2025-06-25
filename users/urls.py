
from django.urls import include, path

from users import views



urlpatterns = [
   path("login",views.login_view,name="user_login")
    
]
