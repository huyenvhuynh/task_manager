from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Discussion, Comment
from courses.models import Course

def discussion_list(request):
    """
    Display a list of discussions for courses the user is enrolled in.
    
    Retrieves discussions related to courses that the current user is enrolled in and
    optionally filters by a selected course if provided through the request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered discussion list template with discussions and user's courses.
    """
    if  request.user.is_authenticated:
        # Check if user is admin
        if request.user.profile.role == 'admin':
            user_courses = Course.objects.all()
        else:
            user_courses = request.user.profile.courses.all()
        selected_course = request.GET.get('course')
    else:
        user_courses = Course.objects.all()
        selected_course = request.GET.get('course')

    # Base queryset for filtering discussions
    discussions = Discussion.objects.filter(course__in=user_courses)

    # Apply course filter if specified
    if selected_course:
        discussions = discussions.filter(course_id=selected_course)

    context = {
        'discussions': discussions,
        'courses': user_courses,
        'selected_course': selected_course,  # To highlight the selected course in the template
    }
    
    return render(request, 'discussions/discussion_list.html', context)

@login_required
def discussion_detail(request, discussion_id):
    """
    Display the details of a specific discussion, including its comments.
    
    If a POST request is received, adds a comment to the discussion.

    Args:
        request (HttpRequest): The HTTP request object.
        discussion_id (int): The ID of the discussion to be displayed.

    Returns:
        HttpResponse: The rendered discussion detail template or redirects back to it after adding a comment.

    Raises:
        Http404: If the discussion with the given ID does not exist or the user is not enrolled in its course.
    """
    discussion = get_object_or_404(
        Discussion, 
        id=discussion_id, 
        course__in=request.user.profile.courses.all()
    )

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment(
                discussion=discussion,
                user=request.user,
                content=content
            )
            comment.save()
        return redirect('discussions:discussion_detail', discussion_id=discussion_id)
    
    return render(request, 'discussions/discussion_detail.html', {'discussion': discussion})

@login_required
def add_discussion(request):
    """
    Handle the creation of a new discussion within a course.
    
    Processes the creation form submitted via POST and validates the course selection
    before creating a discussion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the discussion list page after creation or returns a BadRequest response if the course is invalid.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        course_id = request.POST.get('course')

        # Check if the course is valid for the current user
        try:
            course = request.user.profile.courses.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Invalid course selected.')

        # Create and save the new discussion
        discussion = Discussion(
            title=title,
            content=content,
            course=course,
            user=request.user
        )
        discussion.save()
        return redirect('discussions:discussion_list')

    return redirect('discussions:discussion_list')
