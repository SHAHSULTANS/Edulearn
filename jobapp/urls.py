"""
URL configuration for jobapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    1. Add an import:  from my_app import views
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from jobapp import settings
from django.conf.urls.static import static
from users.views import home_dashboard
# from courses.views import main_hompage


urlpatterns = [
   
    path('admin/', admin.site.urls),
    path("",home_dashboard, name="home"),
    path("user/", include('users.urls')),
    # path('',include('app.urls')),
    # path('',main_hompage,name="index"),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),

    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
