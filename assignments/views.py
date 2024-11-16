"""
Assignment management views for handling CRUD operations and file searching functionality.

This module contains views for managing assignments, including creating, reading,
updating, and deleting assignments, as well as searching through files based on keywords.
Each view handles specific assignment-related functionality with appropriate authentication
and validation checks.
"""

import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from courses.models import Course
from .models import Assignment


def home(request):
    """
    Display the home page if user is authenticated, otherwise redirect to sign in.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered home page or redirect to sign in
    """
    # if request.user.is_authenticated:
    #     return render(request, 'home.html')
    # return redirect('users:sign_in')
    return render(request, 'home.html')


@login_required
def add_assignment(request):
    """
    Handle creation of new assignments with file uploads and metadata.

    Processes POST requests to create new assignments, including file validation
    and metadata handling. Supports file uploads with specific extensions and
    additional metadata like keywords.

    Args:
        request: HttpRequest object containing assignment data

    Returns:
        HttpResponse: Redirect to assignment list on success or error response on failure
    """
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        file_upload = request.FILES.get('file_upload')
        course_id = request.POST.get('course')

        # Validate course
        try:
            course = request.user.profile.courses.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Invalid course selected.')

        # Handle file metadata if file is uploaded
        file_title = request.POST.get('file-title') if file_upload else None
        file_description = request.POST.get('file-description') if file_upload else None
        keywords = request.POST.get('keywords') if file_upload else None

        # Validate file type if present
        if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')

        # Create and save assignment
        assignment = Assignment(
            title=title,
            description=description,
            due_date=due_date,
            file_upload=file_upload,
            file_title=file_title,
            file_description=file_description,
            keywords=keywords,
            user=request.user,
            course=course
        )
        assignment.save()
        return redirect('assignments:assignment_list')
    return redirect('home')


@login_required
def assignment_list(request):
    """
    Display list of assignments for the authenticated user's courses.

    Retrieves and displays all assignments associated with the courses
    the user is enrolled in, including keyword processing for display.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered assignment list page
    """
    user_courses = request.user.profile.courses.all()
    assignments = Assignment.objects.filter(course__in=user_courses)

    # Process keywords for display
    for assignment in assignments:
        if assignment.keywords:
            assignment.keyword_list = [k.strip() for k in assignment.keywords.split(",")]

    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'courses': user_courses
    })


@require_POST
@login_required
def delete_assignment(request, assignment_id):
    """
    Delete an assignment if the user has appropriate permissions.

    Args:
        request: HttpRequest object
        assignment_id: ID of the assignment to delete

    Returns:
        HttpResponse: Redirect to assignment list
    """
    assignment = get_object_or_404(Assignment,
                                id=assignment_id,
                                course__in=request.user.profile.courses.all())
    if assignment.user == request.user:
        assignment.delete()
    return redirect('assignments:assignment_list')


@login_required
def edit_assignment(request, assignment_id):
    """
    Handle editing of existing assignments.

    Allows users to modify their own assignments, including updating files
    and metadata. Includes permission checks and file validation.

    Args:
        request: HttpRequest object
        assignment_id: ID of the assignment to edit

    Returns:
        HttpResponse: Rendered edit form or redirect after successful update
    """
    # Verify permission to edit
    assignment = get_object_or_404(Assignment,
                                id=assignment_id,
                                course__in=request.user.profile.courses.all())
    if assignment.user != request.user:
        return HttpResponseForbidden("You can't edit this assignment")

    if request.method == 'POST':
        # Update assignment data
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        keywords = request.POST.get('keywords')
        file_upload = request.FILES.get('file_upload')
        
        # Update course if provided
        course_id = request.POST.get('course')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                assignment.course = course
            except Course.DoesNotExist:
                return HttpResponseBadRequest('Invalid course.')

        # Handle file upload if provided
        if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
                assignment.file_upload = file_upload
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')

        assignment.keywords = keywords
        assignment.save()
        return redirect('assignments:assignment_list')

    # Display edit form
    user_courses = request.user.profile.courses.all()
    return render(request, 'assignments/edit_assignment.html', {
        'assignment': assignment,
        'courses': user_courses
    })

@login_required
def file_search(request):
    """
    Search assignments based on keywords.

    Filters assignments based on keyword matches and prepares them for display,
    including processing keywords for the template.

    Args:
        request: HttpRequest object containing search query

    Returns:
        HttpResponse: Rendered search results page
    """
    search_query = request.GET.get('q', '').strip().lower()
    
    user_courses = request.user.profile.courses.all()
    assignments = Assignment.objects.filter(course__in=user_courses)

    # Filter assignments based on keyword match
    if search_query:
        filtered_assignments = []
        for assignment in assignments:
            if assignment.keywords:
                keywords = [k.strip().lower() for k in assignment.keywords.split(",")]
                if any(search_query in keyword for keyword in keywords):
                    filtered_assignments.append(assignment)
        assignments = filtered_assignments

    # Process keywords for display
    for assignment in assignments:
        if assignment.keywords:
            assignment.keyword_list = [k.strip() for k in assignment.keywords.split(",")]

    return render(request, 'assignments/file_search.html', {
        'assignments': assignments,
        'courses': user_courses
    })


def calendar(request):
    """
    Display the calendar view.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered calendar page
    """
    return render(request, 'assignments/calendar.html', {})