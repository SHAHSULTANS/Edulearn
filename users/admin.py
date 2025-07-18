# admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import  InstructorProfile, StudentProfile

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)