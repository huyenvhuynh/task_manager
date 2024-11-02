from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Course
from .forms import CourseGroupForm

@login_required
def create_course_group(request):
    if request.method == 'POST':
        form = CourseGroupForm(request.POST)
        if form.is_valid():
            course = form.save()
            group = Group.objects.create(name=course.full_name)
            request.user.groups.add(group)
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseGroupForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile = request.user.profile  # Access the user's profile
    profile.courses.add(course)  # Add the course to the user's profile
    profile.save()  # Save the profile to commit changes
    return redirect('courses:course_list')