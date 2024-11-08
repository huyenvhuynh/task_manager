# assignments/views.py
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from courses.models import Course
from .models import Assignment
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
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
        course_id = request.POST.get('course')  # Get course ID

        try:
            course = request.user.profile.courses.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Invalid course selected.')

        file_title = request.POST.get('file-title') if file_upload else None
        file_description = request.POST.get('file-description') if file_upload else None
        keywords = request.POST.get('keywords') if file_upload else None

        if file_upload:
            validator = FileExtensionValidator(['txt', 'pdf', 'jpg'])
            try:
                validator(file_upload)
            except ValidationError as e:
                return HttpResponseBadRequest('Invalid file type.')

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
    else:
        return redirect('home')

@login_required
def assignment_list(request):
    user_courses = request.user.profile.courses.all()
    assignments = Assignment.objects.filter(course__in=user_courses)

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
    assignment = get_object_or_404(Assignment, 
                                id=assignment_id, 
                                course__in=request.user.profile.courses.all())
    if assignment.user == request.user:
        assignment.delete()
    return redirect('assignments:assignment_list')

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, 
                                id=assignment_id, 
                                course__in=request.user.profile.courses.all())
    if assignment.user != request.user:
        return HttpResponseForbidden("You can't edit this assignment")

    if request.method == 'POST':
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        keywords = request.POST.get('keywords')
        file_upload = request.FILES.get('file_upload')
        
        course_id = request.POST.get('course')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                assignment.course = course
            except Course.DoesNotExist:
                return HttpResponseBadRequest('Invalid course.')

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
    else:
        user_courses = request.user.profile.courses.all()
        return render(request, 'assignments/edit_assignment.html', {
            'assignment': assignment,
            'courses': user_courses
        })

@login_required
def file_search(request):
    search_query = request.GET.get('q', '').strip().lower()
    
    user_courses = request.user.profile.courses.all()
    assignments = Assignment.objects.filter(course__in=user_courses)

    if search_query:
        filtered_assignments = []
        for assignment in assignments:
            if assignment.keywords:
                keywords = [k.strip().lower() for k in assignment.keywords.split(",")]
                if any(search_query in keyword for keyword in keywords):
                    filtered_assignments.append(assignment)
        assignments = filtered_assignments

    for assignment in assignments:
        if assignment.keywords:
            assignment.keyword_list = [k.strip() for k in assignment.keywords.split(",")]

    return render(request, 'assignments/file_search.html', {
        'assignments': assignments,
        'courses': user_courses
    })

def calendar(request):
    return render(request, 'assignments/calendar.html', {})