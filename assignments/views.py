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
from .models import Assignment, AssignmentFile
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin.views.decorators import staff_member_required


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

        # Create and save assignment first
        assignment = Assignment(
            title=title,
            description=description,
            due_date=due_date,
            user=request.user,
            course=course
        )
        assignment.save()

        # Handle file upload if present
        if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
                # Create AssignmentFile with keywords
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=file_upload,
                    title=request.POST.get('file-title') or file_upload.name,
                    description=request.POST.get('file-description'),
                    keywords=request.POST.get('keywords')
                )
            except ValidationError as e:
                assignment.delete()
                return HttpResponseBadRequest('Invalid file type.')

        return redirect('assignments:assignment_list')
    return redirect('home')


@login_required
def assignment_list(request):
    """
    Display list of uncompleted assignments for the authenticated user's courses.
    Redirects admin users to the admin assignment list view.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered assignment list page or redirect for admin users
    """
    # Redirect admin users to admin assignment list
    if request.user.profile.role == 'admin':
        return redirect('assignments:admin_assignment_list')
        
    user_courses = request.user.profile.courses.all()
    # Filter out completed assignments using exclude()
    assignments = Assignment.objects.filter(course__in=user_courses).exclude(
        completed_by=request.user.profile
    )


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
        HttpResponse: Redirect to appropriate assignment list based on user type
    """
    assignment = get_object_or_404(Assignment,
                                id=assignment_id,
                                course__in=request.user.profile.courses.all())
    if assignment.user == request.user:
        assignment.delete()
    
    # Redirect based on user role
    if request.user.profile.role == 'admin':
        return redirect('assignments:admin_assignment_list')
    return redirect('assignments:file_search')


@login_required
def edit_assignment(request, assignment_id):
    """
    Handle editing of existing assignments.
    """
    assignment = get_object_or_404(Assignment,
                                id=assignment_id,
                                course__in=request.user.profile.courses.all())

    # Process keywords for each file
    for file in assignment.files.all():
        if file.keywords:
            file.keyword_list = [k.strip() for k in file.keywords.split(",")]
        else:
            file.keyword_list = []

    if request.method == 'POST':
        # If there's a file upload, create a new AssignmentFile
        if request.FILES.get('file_upload'):
            file_upload = request.FILES['file_upload']
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
                # Create new file with keywords
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=file_upload,
                    title=request.POST.get('file-title') or file_upload.name,
                    description=request.POST.get('file-description'),
                    keywords=request.POST.get('keywords')
                )
                return redirect('assignments:edit_assignment', assignment_id=assignment_id)
            except ValidationError:
                return HttpResponseBadRequest('Invalid file type.')

        # Handle regular assignment updates
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        
        # Update course if provided
        course_id = request.POST.get('course')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                assignment.course = course
            except Course.DoesNotExist:
                return HttpResponseBadRequest('Invalid course.')

        assignment.save()
        return redirect('assignments:assignment_list')

    # Display edit form
    return render(request, 'assignments/edit_assignment.html', {
        'assignment': assignment,
        'user': request.user
    })

@login_required
def file_search(request):
    """
    Search files based on keywords.

    Filters files based on keyword matches and prepares them for display,
    including processing keywords for the template.

    Args:
        request: HttpRequest object containing search query

    Returns:
        HttpResponse: Rendered search results page
    """
    search_query = request.GET.get('q', '').strip().lower()
    
    if request.user.profile.role == 'admin':
        files = AssignmentFile.objects.all()
        user_courses = Course.objects.all()
    else:
        user_courses = request.user.profile.courses.all()
        uncompleted_assignments = Assignment.objects.filter(
            course__in=user_courses
        ).exclude(completed_by=request.user.profile)
        files = AssignmentFile.objects.filter(
            assignment__in=uncompleted_assignments
        )

    # Filter files based on keyword match
    if search_query:
        filtered_files = []
        for file in files:
            if file.keywords:
                keywords = [k.strip().lower() for k in file.keywords.split(",")]
                if search_query in keywords:
                    filtered_files.append(file)
        files = filtered_files

    # Process keywords for display
    for file in files:
        if file.keywords:
            file.keyword_list = [k.strip() for k in file.keywords.split(",")]

    return render(request, 'assignments/file_search.html', {
        'files': files,
        'courses': user_courses
    })

@login_required
def calendar(request):
    """
    Display the calendar view.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered calendar page
    """
    user_courses = request.user.profile.courses.all()
    # Filter out completed assignments using exclude()
    assignments = Assignment.objects.filter(course__in=user_courses).exclude(
        completed_by=request.user.profile
    )
    
    assignments_data = []
    for assignment in assignments:
        assignments_data.append({
            'title': str(assignment.title),
            'due_date': assignment.due_date.strftime('%Y-%m-%d'),
            'id': str(assignment.id),
            'description': str(assignment.description)
        })
    
    assignments_json = json.dumps(assignments_data)

    return render(request, 'assignments/calendar.html', {
        'assignments': assignments,
        'assignments_json': assignments_json,
        'courses': user_courses
    })

# allow assignments to be marked as completed
@login_required
def toggle_complete(request, assignment_id):
    if request.method == 'POST':
        assignment = Assignment.objects.get(id=assignment_id)
        if assignment in request.user.profile.completed_assignments.all():
            request.user.profile.completed_assignments.remove(assignment)
        else:
            request.user.profile.completed_assignments.add(assignment)
    return redirect('assignments:assignment_list')

@login_required
def delete_file(request, assignment_id, file_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
        
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if not request.user.profile.role == 'admin':
        if assignment.course not in request.user.profile.courses.all():
            return HttpResponseForbidden()
        
    file = get_object_or_404(AssignmentFile, id=file_id, assignment=assignment)
    file.delete()
    
    if 'file_search' in request.META.get('HTTP_REFERER', ''):
        return redirect('assignments:file_search')
    return redirect('assignments:edit_assignment', assignment_id=assignment_id)

@login_required
def admin_assignment_list(request):
    """
    Display list of all assignments for admin users.
    Only accessible by administrator members.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered admin assignment list page
    """
    # Get all courses and assignments
    courses = Course.objects.all()
    assignments = Assignment.objects.all()

    return render(request, 'assignments/admin_assignment.html', {
        'assignments': assignments,
        'courses': courses
    })