from django import forms
from django.contrib.auth.models import Group
from .models import Course


class CourseGroupForm(forms.ModelForm):
    """Form for user to create a new group for the course

    Raises:
        forms.ValidationError: If course number isn't 4 digits
        forms.ValidationError: If course name isn't alphanumeric
        forms.ValidationError: If description is too short
        forms.ValidationError: If privacy is not set
        forms.ValidationError: If course with same name and description exists

    Returns:
        CourseGroupForm: Validated course form
    """
    class Meta:
        model = Course
        fields = ['course_name', 'course_number', 'description', 'privacy']
        widgets = {
            'privacy': forms.Select(
                choices=[
                    (True, 'Private'),
                    (False, 'Public')
                ],
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter course description...'
                }
            ),
            'course_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter course name'
                }
            ),
            'course_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter 4-digit course number'
                }
            )
        }

    def clean_privacy(self):
        privacy = self.cleaned_data.get('privacy')
        if privacy is None:
            raise forms.ValidationError("Course must be set to either private or public")
        return privacy

    def clean_course_number(self):
        number = self.cleaned_data['course_number']
        if number < 1000 or number > 9999:  
            raise forms.ValidationError("Course number must be a 4-digit number")
        return number
        
    def clean_course_name(self):  
        name = self.cleaned_data['course_name'] 
        if len(name) >= 5 or len(name) < 1: 
            raise forms.ValidationError("Course name must be 4 characters or less")
        if not name.isalnum():
            raise forms.ValidationError("Course name must be alphanumeric")
        return name.upper()
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Course description is required")
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long")
        return description
    
    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get('course_name')
        course_number = cleaned_data.get('course_number')
        description = cleaned_data.get('description')
        
        if course_name and course_number and description:
            full_name = f'{course_name} {course_number}'
            # Check for duplicate course with same name and description
            if Course.objects.filter(
                full_name=full_name,
                description=description
            ).exists():
                raise forms.ValidationError(
                    f"A course with the name '{full_name}' and identical description already exists."
                )
        return cleaned_data


class CourseDescriptionForm(forms.ModelForm):
    """Form for editing only the description of an existing course

    Raises:
        forms.ValidationError: If description is too short or empty

    Returns:
        CourseDescriptionForm: Validated description form
    """
    class Meta:
        model = Course
        fields = ['description']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter course description...'
                }
            )
        }
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Course description is required")
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long")
        return description

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        
        # Check if description is identical to another course with same name
        if description and hasattr(self.instance, 'full_name'):
            if Course.objects.exclude(id=self.instance.id).filter(
                full_name=self.instance.full_name,
                description=description
            ).exists():
                raise forms.ValidationError(
                    "A course with this name and identical description already exists."
                )
        return cleaned_data