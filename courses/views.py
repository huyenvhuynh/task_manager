"""
Course management views for handling course-related operations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone
from .models import Course, EnrollmentRequest
from .forms import CourseGroupForm, CourseDescriptionForm


@login_required
def create_course_group(request):
    """
    Create a new course and associated permission group.
    
    Handles the creation of a new course using the CourseGroupForm and automatically
    creates a corresponding Django auth Group for permission management. The creating
    user is automatically added to the new group and enrolled in the course.
    
    Args:
        request: HttpRequest object containing course creation form data
        
    Returns:
        HttpResponse: Redirects to course detail page on successful creation,
                     or renders the creation form with errors if invalid
    """
    if request.method == 'POST':
        form = CourseGroupForm(request.POST)
        if form.is_valid():
            # Create the course and set creator
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            
            # Create a unique group name and get or create the group
            group_name = f"{course.full_name}_{course.id}"
            group, created = Group.objects.get_or_create(name=group_name)
            
            # Add user to group
            request.user.groups.add(group)
            
            # Auto-enroll the creator
            course.enrolled_users.add(request.user)
            request.user.profile.courses.add(course)
            
            messages.success(request, f"Successfully created and enrolled in {course.full_name}")
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseGroupForm()
    
    return render(request, 'courses/create_course.html', {'form': form})

def course_detail(request, pk):
    """Display detailed information about a specific course."""
    course = get_object_or_404(Course, pk=pk)
    user_has_access = (
        request.user.is_authenticated and (
            request.user == course.creator or 
            not course.privacy or 
            request.user in course.enrolled_users.all()
        )
    )
    
    enrollment_request = None
    if request.user.is_authenticated:
        enrollment_request = EnrollmentRequest.objects.filter(
            course=course, 
            user=request.user
        ).first()
        
    pending_requests = []
    if request.user.is_authenticated and request.user == course.creator:
        pending_requests = EnrollmentRequest.objects.filter(
            course=course,
            status='PENDING'
        )
    
    context = {
        'course': course,
        'user_has_access': user_has_access,
        'enrollment_request': enrollment_request,
        'is_creator': request.user.is_authenticated and request.user == course.creator,
        'pending_requests': pending_requests
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def request_enrollment(request, course_id):
    """Handle requests for enrollment in a private course."""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user == course.creator:
        messages.error(request, "You cannot request enrollment in your own course.")
        return redirect('courses:course_detail', pk=course_id)
        
    if request.user in course.enrolled_users.all():
        messages.info(request, "You are already enrolled in this course.")
        return redirect('courses:course_detail', pk=course_id)
        
    enrollment_request, created = EnrollmentRequest.objects.get_or_create(
        course=course,
        user=request.user,
        defaults={'status': 'PENDING'}
    )
    
    if created:
        messages.success(request, "Enrollment request sent successfully.")
    else:
        messages.info(request, "You already have a pending request for this course.")
        
    return redirect('courses:course_detail', pk=course_id)

@login_required
def manage_enrollment_request(request, request_id, action):
    """
    Handle enrollment request approval/rejection and update user enrollment status.
    """
    enrollment_request = get_object_or_404(EnrollmentRequest, pk=request_id)
    course = enrollment_request.course
    
    if request.user != course.creator:
        messages.error(request, "You don't have permission to manage enrollment requests.")
        return redirect('courses:course_detail', pk=course.pk)
    
    if action == 'approve':
        enrollment_request.status = 'APPROVED'
        enrollment_request.response_date = timezone.now()
        enrollment_request.save()
        
        # Add user to enrolled_users of the course
        course.enrolled_users.add(enrollment_request.user)
        
        # Add course to user's profile
        enrollment_request.user.profile.courses.add(course)
        
        messages.success(request, f"Enrollment request from {enrollment_request.user.username} approved.")
    elif action == 'reject':
        enrollment_request.status = 'REJECTED'
        enrollment_request.response_date = timezone.now()
        enrollment_request.save()
        messages.success(request, f"Enrollment request from {enrollment_request.user.username} rejected.")
    
    return redirect('courses:course_detail', pk=course.pk)

def course_list(request):
    """Display a list of all available courses."""
    # Redirect admin users to the admin course view
    if request.user.is_authenticated and request.user.profile.role == 'admin':
        return redirect('courses:admin_course')
        
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def enroll_in_course(request, course_id):
    """Handle direct enrollment for public courses and creator re-enrollment."""
    course = get_object_or_404(Course, id=course_id)
    
    # Allow creator to always re-enroll
    if request.user == course.creator:
        request.user.profile.courses.add(course)
        course.enrolled_users.add(request.user)
        messages.success(request, f"Successfully re-enrolled in your course {course.full_name}")
        return redirect('courses:course_list')
        
    if course.privacy and request.user != course.creator:
        # Redirect to request enrollment for private courses
        return redirect('courses:request_enrollment', course_id=course_id)
        
    request.user.profile.courses.add(course)
    course.enrolled_users.add(request.user)
    messages.success(request, f"Successfully enrolled in {course.full_name}")
    return redirect('courses:course_list')

@login_required
def unenroll_from_course(request, course_id):
    """Handle unenrollment from courses."""
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        # Remove from profile's courses
        request.user.profile.courses.remove(course)
        # Remove from course's enrolled_users
        course.enrolled_users.remove(request.user)
        messages.success(request, f"Successfully unenrolled from {course.full_name}")
    return redirect('courses:course_list')

@login_required
def delete_course(request, course_id):
    """
    Delete a course. Only the course creator or admin can delete the course.
    """
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course creator or an admin
    if request.user != course.creator and request.user.profile.role != 'admin':
        messages.error(request, "You don't have permission to delete this course.")
        return redirect('courses:course_detail', pk=course_id)
    
    if request.method == 'POST':
        course_name = course.full_name
        course.delete()
        messages.success(request, f"Course '{course_name}' has been deleted.")
        
        # Redirect admins back to admin course list
        if request.user.profile.role == 'admin':
            return redirect('courses:admin_course')
        return redirect('courses:course_list')
        
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
def edit_course_description(request, course_id):
    """Edit a course description. Only the course creator can edit the description."""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course creator
    if request.user != course.creator:
        messages.error(request, "You don't have permission to edit this course.")
        return redirect('courses:course_detail', pk=course_id)
    
    if request.method == 'POST':
        form = CourseDescriptionForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course description updated successfully.")
            return redirect('courses:course_detail', pk=course_id)
    else:
        form = CourseDescriptionForm(instance=course)
        
    return render(request, 'courses/edit_course_description.html', {
        'form': form,
        'course': course
    })

@login_required
def admin_course(request):
    """
    Display all courses in an admin view.
    Only accessible to authenticated users.
    """
    courses = Course.objects.all().order_by('course_number')
    return render(request, 'admin_course.html', {'courses': courses})