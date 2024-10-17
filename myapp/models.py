from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    file_upload = models.FileField(
        upload_to='assignments/',
        validators=[FileExtensionValidator(['txt', 'pdf', 'jpg'])],
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
