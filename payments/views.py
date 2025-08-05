from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from courses.models import Course
from .models import Payment
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        price = course.discounted_price if course.discounted_price else course.price
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(price * 100),  # Convert to cents
                            'product_data': {
                                'name': course.title,
                                'description': course.description[:200],
                                'images': [request.build_absolute_uri(course.thumbnail.url)] if course.thumbnail else [],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('payments:success', kwargs={'pk': course.id})
                ),
                cancel_url=request.build_absolute_uri(
                    reverse('courses:course_detail', kwargs={'pk': course.id})
                ),
                metadata={
                    'course_id': course.id,
                    'user_id': request.user.id,
                },
            )
            
            # Create a pending payment record
            Payment.objects.create(
                student=request.user,
                course=course,
                amount=price,
                payment_method='stripe',
                status='pending',
                stripe_checkout_id=checkout_session.id
            )
            
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            messages.error(request, f"Payment initiation failed: {str(e)}")
            return redirect('courses:course_detail', pk=course.id)

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['course'] = course
        return context

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        payment = Payment.objects.filter(
            student=request.user, 
            course=course, 
            status='pending'
        ).first()
        
        if payment:
            payment.status = 'completed'
            payment.save()
            
            # Enroll student
            Enrollment.objects.get_or_create(
                student=request.user,
                course=course
            )
            messages.success(request, f"Successfully enrolled in {course.title}!")
        
        return super().get(request, *args, **kwargs)

class PaymentCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['course'] = course
        return context