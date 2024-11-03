from django import forms
from django.contrib.auth.models import Group
from .models import Course


class CourseGroupForm(forms.ModelForm):
    """Form for user to create a new group for the course

    Raises:
        forms.ValidationError: If course number isn't 4 digits
        forms.ValidationError: If course name isn't alphanumeric

    Returns:
        CourseGroupForm: Validated course form
    """
    class Meta:
        model = Course
        fields = ['course_name', 'course_number']
        
    def clean_course_number(self):
        number = self.cleaned_data['course_number']
        if number < 1000 or number > 9999:  
            raise forms.ValidationError("Course number must be a 4-digit number")
        return number
        
    def clean_course_name(self):  
        name = self.cleaned_data['course_name']  
        if not name.isalnum():
            raise forms.ValidationError("Course name must be alphanumeric")
        return name.upper()