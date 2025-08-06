from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView

app_name = 'reviews'

urlpatterns = [
    path('course/<int:pk>/review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('course/<int:course_id>/review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]