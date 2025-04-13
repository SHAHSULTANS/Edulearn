





from django.urls import path


from app import views
from app.views import job_list, jobDetails



urlpatterns = [
    path('',job_list,name="job-home"),
    path('hello/',views.hello, name='hello'),
    path('job/<int:id>',jobDetails, name="jobs-detail"),
]
