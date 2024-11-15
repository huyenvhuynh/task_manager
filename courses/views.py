"""
Course management views for handling course-related operations.

This module provides views for managing courses, including creation of course groups,
viewing course details, listing courses, and handling course enrollment. Each view
requires user authentication and handles specific course-related functionality.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Course
from .forms import CourseGroupForm


@login_required
def create_course_group(request):
    """
    Create a new course and associated permission group.
    
    Handles the creation of a new course using the CourseGroupForm and automatically
    creates a corresponding Django auth Group for permission management. The creating
    user is automatically added to the new group.
    
    Args:
        request: HttpRequest object containing course creation form data
        
    Returns:
        HttpResponse: Redirects to course detail page on successful creation,
                     or renders the creation form with errors if invalid
    """
    if request.method == 'POST':
        form = CourseGroupForm(request.POST)
        if form.is_valid():
            # Create the course from form data
            course = form.save()
            
            # Create and associate a permission group
            group = Group.objects.create(name=course.full_name)
            request.user.groups.add(group)
            
            return redirect('courses:course_detail', pk=course.pk)
    else:
        # Display empty form for GET requests
        form = CourseGroupForm()
    
    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def course_detail(request, pk):
    """
    Display detailed information about a specific course.
    
    Retrieves and displays all information associated with a specific course.
    Raises 404 if the course doesn't exist.
    
    Args:
        request: HttpRequest object
        pk: Primary key of the course to display
        
    Returns:
        HttpResponse: Rendered course detail page
        
    Raises:
        Http404: If the course with given pk doesn't exist
    """
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


# @login_required
def course_list(request):
    """
    Display a list of all available courses.
    
    Retrieves and displays all courses in the system. No filtering is applied,
    so all courses are visible to authenticated users.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Rendered course list page containing all courses
    """
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def enroll_in_course(request, course_id):
    """
    Handle user enrollment in a specific course.
    
    Adds the specified course to the user's profile, effectively enrolling them
    in the course. Raises 404 if the course doesn't exist.
    
    Args:
        request: HttpRequest object
        course_id: ID of the course to enroll in
        
    Returns:
        HttpResponse: Redirects to course list page after successful enrollment
        
    Raises:
        Http404: If the course with given course_id doesn't exist
    """
    # Retrieve the course or return 404 if not found
    course = get_object_or_404(Course, id=course_id)
    
    # Get the user's profile and add the course
    profile = request.user.profile
    profile.courses.add(course)
    
    # Save changes to the profile
    profile.save()
    
    return redirect('courses:course_list')