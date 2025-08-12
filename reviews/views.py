from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from courses.models import Course, Enrollment
from .models import Review, ReviewVote
from .forms import ReviewForm

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        # Check if user is enrolled
        if not Enrollment.objects.filter(student=request.user, course=self.course).exists():
            messages.warning(request, "You must enroll in the course before reviewing")
            return redirect('course_detail', pk=self.course.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.course = self.course
        form.instance.user = self.request.user
        form.instance.is_verified = True  # Mark as verified purchase
        messages.success(self.request, "Your review has been submitted!")
        return super().form_valid(form)

def vote_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    is_helpful = request.POST.get('is_helpful') == 'true'
    
    # Update or create vote
    vote, created = ReviewVote.objects.update_or_create(
        review=review,
        user=request.user,
        defaults={'is_helpful': is_helpful}
    )
    
    # Update helpful count
    review.helpful_count = review.votes.filter(is_helpful=True).count()
    review.save()
    
    return JsonResponse({
        'helpful_count': review.helpful_count,
        'user_vote': is_helpful
    })