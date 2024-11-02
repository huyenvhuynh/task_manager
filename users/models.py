from django.conf import settings
from django.db import models
from courses.models import Course

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('user', 'Common User'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    image = models.ImageField(upload_to='jpg/', default='default.jpg')
    courses = models.ManyToManyField(Course, related_name='profiles', blank=True) # Adds course to user profile 

    def __str__(self):
        return f"{self.user.email} - {self.role}"