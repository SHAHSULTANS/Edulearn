from django.urls import path
from .views import CreateCheckoutSessionView, PaymentSuccessView, PaymentCancelView

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:pk>/', CreateCheckoutSessionView.as_view(), name='checkout'),
    path('success/<int:pk>/', PaymentSuccessView.as_view(), name='success'),
    path('cancel/<int:pk>/', PaymentCancelView.as_view(), name='cancel'),
]
