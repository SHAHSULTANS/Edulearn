from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from courses.models import Course
from django.contrib.auth import get_user_model
User=get_user_model()

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆ (Poor)'),
        (2, '★★☆☆☆ (Fair)'), 
        (3, '★★★☆☆ (Good)'),
        (4, '★★★★☆ (Very Good)'),
        (5, '★★★★★ (Excellent)'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120)
    content = models.TextField()
    helpful_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)  # Indicates if the reviewer purchased the course
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'user')  # Prevent duplicate reviews per user per course
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s review on '{self.course.title}' ({self.rating}★)"


class ReviewVote(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_votes'
    )
    is_helpful = models.BooleanField()  # True = helpful, False = not helpful
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')  # Only one vote per user per review

    def __str__(self):
        status = "Helpful" if self.is_helpful else "Not Helpful"
        return f"{self.user.username} voted {status} on Review #{self.review.id}"
