from django.contrib import admin
from .models import Course, Category, Section

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'instructor', 'category', 'price',
        'level', 'is_published', 'created_at',
    )
    list_filter = ('level', 'is_published', 'category', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    autocomplete_fields = ('instructor', 'category', 'students')
    filter_horizontal = ('students',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Section)