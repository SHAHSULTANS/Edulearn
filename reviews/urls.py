from django.urls import path
from .views import CreateReviewView

app_name = 'reviews'

urlpatterns = [
    path('course/<int:course_id>/review/create/', CreateReviewView.as_view(), name='review_create'),
    # path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    # path('course/<int:course_id>/review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]