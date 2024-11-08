from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .storages import AssignmentStorage
from courses.models import Course

class Assignment(models.Model):
    """
    Represents an assignment created by a user and associated with a course.

    Attributes:
        title (CharField): The title of the assignment.
        description (TextField): A detailed description of the assignment.
        due_date (DateField): The due date for the assignment submission.
        file_upload (FileField): An optional file upload related to the assignment, 
            stored with a custom storage backend and validated for specific file extensions.
        user (ForeignKey): The user who created the assignment, linked via a foreign key.
        course (ForeignKey): The course to which the assignment belongs, linked via a foreign key.
        uploaded_at (DateTimeField): The timestamp indicating when the assignment was uploaded.
        file_title (CharField): An optional title for the uploaded file.
        file_description (TextField): An optional description for the uploaded file.
        keywords (CharField): Optional, comma-separated keywords for the assignment, aiding in categorization or search.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    file_upload = models.FileField(
        upload_to='',
        storage=AssignmentStorage(),
        validators=[FileExtensionValidator(['txt', 'pdf', 'jpg'])],
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_title = models.CharField(max_length=255, null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated keywords")

    def __str__(self) -> str:
        """
        Return the string representation of the assignment.

        Returns:
            str: The title of the assignment.
        """
        return self.title
