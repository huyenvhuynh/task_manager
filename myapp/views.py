# views.py
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import Assignment
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return redirect('users:sign_in')

@login_required
def add_assignment(request):
    if request.method == 'POST':
        # Get data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        file_upload = request.FILES.get('file_upload')
        
        # Only get metadata if there's a file
        file_title = request.POST.get('file-title') if file_upload else None
        file_description = request.POST.get('file-description') if file_upload else None
        keywords = request.POST.get('keywords') if file_upload else None

        # Verify the file extension if file exists
        if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')

        # Create an assignment with the form data
        assignment = Assignment(
            title=title,
            description=description,
            due_date=due_date,
            file_upload=file_upload,
            file_title=file_title,
            file_description=file_description,
            keywords=keywords,
            user=request.user
        )
        assignment.save()
        return redirect('myapp:assignment_list')  # Use namespaced URL
    else:
        return redirect('myapp:home')

@login_required
def assignment_list(request):
    # Fetch assignments belonging to the logged-in user
    assignments = Assignment.objects.filter(user=request.user)

    # Split keywords for each assignment
    for assignment in assignments:
        if assignment.keywords:
            # Split on comma and strip whitespace from each keyword
            assignment.keyword_list = [k.strip() for k in assignment.keywords.split(",")]

    return render(request, 'myapp/assignment_list.html', {'assignments': assignments})

@require_POST  
@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
    assignment.delete()
    return redirect('myapp:assignment_list')

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
    if request.method == 'POST':
        # Update fields with new data
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        keywords = request.POST.get('keywords')
        file_upload = request.FILES.get('file_upload')

        if file_upload:
            # Validate the new file
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
                assignment.file_upload = file_upload
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')

        assignment.keywords = keywords
        assignment.save()
        return redirect('myapp:assignment_list')  
    else:
        return render(request, 'myapp/edit_assignment.html', {'assignment': assignment})
    

@login_required
def file_search(request):
    # Get search query from 
    search_query = request.GET.get('q', '').strip().lower()
    
    # Fetch assignments belonging to the logged-in user
    assignments = Assignment.objects.filter(user=request.user)

    # Filter assignments if there's a search query
    if search_query:
        filtered_assignments = []
        for assignment in assignments:
            if assignment.keywords:
                # Split on comma and strip whitespace from each keyword
                keywords = [k.strip().lower() for k in assignment.keywords.split(",")]
                if any(search_query in keyword for keyword in keywords):
                    filtered_assignments.append(assignment)
        assignments = filtered_assignments

    # Split keywords for each assignment
    for assignment in assignments:
        if assignment.keywords:
            # Split on comma and strip whitespace from each keyword
            assignment.keyword_list = [k.strip() for k in assignment.keywords.split(",")]

    return render(request, 'myapp/file_search.html', {'assignments': assignments})
