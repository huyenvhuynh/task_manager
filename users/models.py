from django.conf import settings
from django.db import models
from courses.models import Course
from assignments.models import Assignment

class Profile(models.Model):
    """
    Represents a user profile in the system, linked to a user and associated with courses.

    Attributes:
        user (OneToOneField): A one-to-one relationship linking this profile to a user account.
        role (CharField): The role of the user, which can be 'admin' or 'user' or 'anonymous', with 'user' as the default.
        image (ImageField): The profile image of the user, stored in the 'jpg/' directory, with 'default.jpg' as the default image.
        courses (ManyToManyField): A many-to-many relationship linking this profile to multiple courses.
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('user', 'Common User'),
        ('anonymous', 'Guest'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='anonymous')
    image = models.ImageField(upload_to='jpg/', default='default.jpg')
    courses = models.ManyToManyField(Course, related_name='profiles', blank=True)  

    completed_assignments = models.ManyToManyField(Assignment, related_name='completed_by', blank=False)

    def __str__(self) -> str:
        """
        Return the string representation of the profile.

        Returns:
            str: A string in the format '<user email> - <role>'.
        """
        return f"{self.user.email} - {self.role}"
