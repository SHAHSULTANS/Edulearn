# Generated by Django 5.1.3 on 2025-04-07 13:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lesson',
            name='completion_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='completed_lessons',
            field=models.ManyToManyField(blank=True, related_name='completed_by', to='courses.lesson'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='course_thumbnails/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrolled_courses',
            field=models.ManyToManyField(blank=True, related_name='students', to='courses.course'),
        ),
    ]
