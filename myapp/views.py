import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import Assignment
from django.core.validators import FileExtensionValidator
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return redirect('users:sign_in')
    
@login_required
def add_assignment(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', '/') # this is so we redirect to the original page after adding the assignment

    # this gets data from the form
    title = request.POST.get('title')
    description = request.POST.get('description')
    due_date = request.POST.get('due_date')
    file_upload = request.FILES.get('file_upload')
    file_upload = request.FILES.get('file_upload')

    # this verifies that the file extension is one of the required ones
    if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')
    
    # this creates an assignment with the data from the form
    assignment = Assignment(
        title=title,
        description=description,
        due_date=due_date,
        file_upload=file_upload,
        user=request.user
    )
    # save assignment to database
    assignment.save()
    return redirect(next_url)
