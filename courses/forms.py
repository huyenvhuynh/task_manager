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
        if len(name) >= 4: 
             raise forms.ValidationError("Course name must be 4 characters or less")
        if not name.isalnum():
            raise forms.ValidationError("Course name must be alphanumeric")
        return name.upper()
    
    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get('course_name')
        course_number = cleaned_data.get('course_number')
        if course_name and course_number:
            full_name = f'{course_name} {course_number}'
            if Course.objects.filter(full_name=full_name).exists():
                raise forms.ValidationError(f"The course '{full_name}' already exists.")
        return cleaned_data