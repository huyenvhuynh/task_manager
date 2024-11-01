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
        keywords = request.POST.get('keywords')  # Retrieve keywords as comma-separated string


        # Verify the file extension
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
            assignment.keyword_list = assignment.keywords.split(",")  # Add a new attribute to store split keywords

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
