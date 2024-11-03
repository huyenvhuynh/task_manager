from django.db import models


class Course(models.Model):
    """
    Represents a course offered in the system with a unique course number and name.

    Attributes:
        course_number (BigIntegerField): The unique identifier for the course, typically assigned by the institution.
        course_name (CharField): The name of the course, up to 200 characters.

    Properties:
        full_name (str): Returns the concatenated course name and course number for a complete identifier.

    Methods:
        __str__: Returns the full_name for the course as a string representation.
    """
    course_number = models.BigIntegerField()
    course_name = models.CharField(max_length=200)

    @property
    def full_name(self):
        return f'{self.course_name} {self.course_number}'

    def __str__(self):
        return self.full_name
