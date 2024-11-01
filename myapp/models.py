from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .storages import AssignmentStorage

# this model is used to store the assignments that the user creates
class Assignment(models.Model):
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
    uploaded_at = models.DateTimeField(auto_now_add=True)
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")


    def __str__(self):
        return self.title
