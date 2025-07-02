
from django.urls import include, path

from users import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
   path('login/', views.UserLoginView.as_view(), name='login'),
   path('logout/', views.custom_logout_view, name='logout'),
   path('register/', views.register, name='register'),
   path('terms/', views.terms_of_service, name='terms_of_service'),
   path('privacy/', views.privacy_policy, name='privacy_policy'),
    
]






from django.contrib.auth import views as auth_views
urlpatterns += [
    # Forgot Password URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password/reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password/reset_complete.html'), name='password_reset_complete'),
]

