from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import CourseGroupForm


def create_course_group(request):
    if request.method == 'POST':
        form = CourseGroupForm(request.POST)
        if form.is_valid():
            course = form.save()
            group = Group.objects.create(name=course.full_name)
            request.user.groups.add(group)
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseGroupForm()
    
    return render(request, 'courses/create_course.html', {'form': form})