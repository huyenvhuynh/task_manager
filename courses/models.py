from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """
    Represents a course offered in the system with a unique course number and name.

    Attributes:
        course_number (BigIntegerField): The unique identifier for the course, typically assigned by the institution.
        course_name (CharField): The name of the course, up to 200 characters.

    Properties:
        full_name (str): Concatenated course name and course number for a complete identifier.
    """
    course_name = models.CharField(max_length=200)
    course_number = models.IntegerField()
    description = models.TextField(
        max_length=1000,
        help_text="Detailed description of the course content and objectives",
        default=None,
    )
    full_name = models.CharField(max_length=255, unique=False, default='')
    privacy = models.BooleanField(
        choices=[
            (True, 'Private'),
            (False, 'Public')
        ],
        default=None,
        null=True,
        help_text="Specify if the course is private or public"
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_courses',
        default=None
    )
    enrolled_users = models.ManyToManyField(
        User, 
        related_name='enrolled_courses', 
        blank=True,
        default=None
    )

    def save(self, *args, **kwargs):
        self.full_name = f'{self.course_name} {self.course_number}'
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'description'],
                name='unique_course_with_description'
            )
        ]

class EnrollmentRequest(models.Model):
    """
    Represents a request to enroll in a private course.
    
    Attributes:
        course: The course being requested to enroll in
        user: The user requesting enrollment
        status: Current status of the request (PENDING, APPROVED, REJECTED)
        request_date: When the request was made
        response_date: When the request was responded to
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollment_requests'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='course_requests'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['course', 'user']