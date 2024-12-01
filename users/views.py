"""
Authentication views for handling Google OAuth2 sign-in and user management.

This module provides views for managing user authentication through Google OAuth2,
including sign-in, sign-out, role selection, and token verification. It handles
user creation, session management, and role-based access control.

Dependencies:
    - google.oauth2: For token verification
    - django.contrib.auth: For user authentication
    - django.contrib.auth.models: For user management
"""

import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


@csrf_exempt
def google_sign_in(request):
    """
    Render the Google sign-in page with OAuth2 client credentials.

    Provides the necessary Google OAuth2 client ID for the frontend to initiate
    the authentication flow.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Rendered sign-in template with Google client ID in context.
    """
    return render(request, 'users/sign_in.html', {
        'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    })


def sign_in(request):
    """
    Handle user sign-in and display appropriate messages.

    For authenticated users, displays a role-specific success message and user details.
    For unauthenticated users, shows the sign-in page with Google OAuth2 credentials.

    Args:
        request (HttpRequest): The incoming request object containing user session data.

    Returns:
        HttpResponse: Rendered template with either:
            - Success message and user details for authenticated users
            - Sign-in form with Google client ID for unauthenticated users
    """
    if request.user.is_authenticated:
        # Determine user role and set appropriate message
        profile = request.user.profile
        message = (
            "Successfully signed in as an Administrator!"
            if profile.role == 'admin'
            else "Successfully signed in as a Common User!"
        )
        
        context = {
            'message': message,
            'email': request.user.email,
            'name': request.user.get_full_name(),
        }
    else:
        context = {
            'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        }
    
    return render(request, 'users/sign_in.html', context)


@csrf_exempt
def auth_receiver(request):
    """
    Process Google OAuth2 authentication callback and handle user creation/login.

    Verifies the OAuth2 token, extracts user information, and either creates a new
    user or logs in an existing user. Handles session management and redirects
    based on user status.

    Args:
        request (HttpRequest): The incoming request containing the OAuth2 token.

    Returns:
        HttpResponse: One of the following:
            - Redirect to role selection for new users
            - Redirect to sign-in page for existing users
            - 400 error for missing token
            - 403 error for invalid token
            - 405 error for invalid request method

    Raises:
        ValueError: If the OAuth2 token verification fails
    """
    if request.method != 'POST':
        return HttpResponse('Invalid request method', status=405)

    token = request.POST.get('credential')
    if not token:
        return HttpResponse('No token provided', status=400)

    try:
        # Verify Google OAuth2 token
        user_data = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse('Invalid token', status=403)

    # Process user information
    email = user_data.get('email')
    name = user_data.get('name', '')
    name_parts = name.split(' ')
    first_name = name_parts[0] if name_parts else ''
    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

    # Create or retrieve user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
    )

    # Handle user session
    login(request, user)
    request.session['user_data'] = {
        'email': email,
        'name': f"{first_name} {last_name}"
    }

    return redirect('users:select_role' if created else 'users:sign_in')


@login_required
def select_role(request):
    """
    Handle user role selection and profile updates.

    Processes role selection for new users and updates their profile accordingly.
    Only accepts 'admin' or 'user' as valid roles.

    Args:
        request (HttpRequest): The incoming request, must be authenticated.

    Returns:
        HttpResponse: One of the following:
            - Rendered sign-in page with success message after role selection
            - Rendered role selection form for GET requests
            - 400 error for invalid role selection

    Notes:
        - Requires user authentication (@login_required)
        - Updates both profile and session data with selected role
    """
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        if selected_role not in ['admin', 'user']:
            return HttpResponse('Invalid role selection', status=400)

        # Update user profile and session
        request.user.profile.role = selected_role
        request.user.profile.save()

        # Ensure and update session data
        if 'user_data' not in request.session:
            request.session['user_data'] = {}
        request.session['user_data']['role'] = selected_role

        # Create role-specific success message
        message = (
            "Successfully signed in as an Administrator!"
            if selected_role == 'admin'
            else "Successfully signed in as a Common User!"
        )

        return render(request, 'users/sign_in.html', {
            'message': message,
            'email': request.user.email,
            'name': request.user.get_full_name(),
        })

    return render(request, 'users/select_role.html')


def sign_out(request):
    """
    Handle user sign-out and session cleanup.

    Clears user session data and logs out the user, maintaining clean session state.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Redirect to sign-in page after successful logout.

    Notes:
        - Safely removes session data using .pop()
        - Performs Django logout to clear authentication
    """
    request.session.pop('user_data', None)
    logout(request)
    return redirect('users:sign_in')

def anonymous(request):
    """
    Handle anonymous user experience

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Redirect to sign-in page after successful logout.
    """

    return render(request, 'home.html', {})

def about(request):
    return render(request, 'users/about.html', {})

def locked(request):
    """
    Prevents anonymous users from accessing protected pages

    Args:
        request (HttpRequest): The incoming request object.
    """
    return render(request, 'users/locked.html', {})

@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)