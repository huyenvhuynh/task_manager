from django.db import models

class Course(models.Model):
    """
    Represents a course offered in the system with a unique course number and name.

    Attributes:
        course_number (BigIntegerField): The unique identifier for the course, typically assigned by the institution.
        course_name (CharField): The name of the course, up to 4 characters.

    Properties:
        full_name (str): Concatenated course name and course number for a complete identifier.

    Methods:
        __str__() -> str: Returns the full name of the course as a string representation.
    """
    course_number = models.BigIntegerField()
    course_name = models.CharField(max_length=4)

    @property
    def full_name(self) -> str:
        """
        str: The full name of the course, combining the course name and course number.
        """
        return f'{self.course_name} {self.course_number}'

    def __str__(self) -> str:
        """
        Returns the string representation of the course.

        Returns:
            str: The full name of the course.
        """
        return self.full_name
