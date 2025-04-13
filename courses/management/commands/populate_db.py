import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from courses.models import Course, Lesson  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Creates and updates fake courses and lessons data with thumbnails'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create some courses if they don't exist, or update them
        for _ in range(5):  # Create 5 courses
            course_title = fake.catch_phrase()
            course, created = Course.objects.update_or_create(
                title=course_title,
                defaults={
                    'description': fake.paragraph(nb_sentences=5),
                    'duration': random.randint(4, 40),
                    'created_at': timezone.now(),
                    'thumbnail': f"https://picsum.photos/200/200?random={random.randint(1, 1000)}",  # Fake image URL
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course_title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated course: {course_title}'))

            # Create lessons for each course
            num_lessons = random.randint(3, 6)  # 3-6 lessons per course
            for _ in range(num_lessons):
                lesson_title = fake.sentence(nb_words=4)
                lesson, lesson_created = Lesson.objects.update_or_create(
                    course=course,
                    title=lesson_title,
                    defaults={
                        'content': fake.paragraph(nb_sentences=10),
                        'video_url': fake.url() if random.choice([True, False]) else None,
                        'completion_status': random.choice([True, False])
                    }
                )
                if lesson_created:
                    self.stdout.write(self.style.SUCCESS(f'Created lesson: {lesson_title}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated lesson: {lesson_title}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created and updated courses with lessons'))
