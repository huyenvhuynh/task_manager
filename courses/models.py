from django.db import models

class Course(models.Model):
    """
    Represents a course offered in the system with a unique course number and name.

    Attributes:
        course_number (BigIntegerField): The unique identifier for the course, typically assigned by the institution.
        course_name (CharField): The name of the course, up to 200 characters.

    Properties:
        full_name (str): Concatenated course name and course number for a complete identifier.
    """
    course_number = models.BigIntegerField()
    course_name = models.CharField(max_length=200)

    @property
    def full_name(self) -> str:
        """
        Return the full name of the course.

        Returns:
            str: The course name concatenated with the course number.
        """
        return f'{self.course_name} {self.course_number}'

    def __str__(self) -> str:
        """
        Return the string representation of the course.

        Returns:
            str: The full name of the course.
        """
        return self.full_name
