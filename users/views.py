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
    Render the Google sign-in page with the Google client ID.

    The view renders a template that provides the necessary client ID for Google OAuth2.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered sign-in page with the client ID context.
    """
    return render(request, 'users/sign_in.html', {
        'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    })

def sign_in(request):
    """
    Display the sign-in page or a success message if the user is already authenticated.

    Checks if the user is authenticated and displays a success message with user details
    or renders the sign-in page if not authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered sign-in page or a page with user-specific details.
    """
    if request.user.is_authenticated:
        # Retrieve the user's profile and determine the role-based message
        profile = request.user.profile  
        if profile.role == 'admin':
            message = "Successfully signed in as an Administrator!"
        else:
            message = "Successfully signed in as a Common User!"
        
        context = {
            'message': message,
            'email': request.user.email,
            'name': request.user.get_full_name(),
        }
    else:
        # User is not authenticated, show the sign-in page with the Google client ID
        context = {
            'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        }
    
    return render(request, 'users/sign_in.html', context)

@csrf_exempt
def auth_receiver(request):
    """
    Handle the authentication process from the Google OAuth2 callback.

    Verifies the received token, retrieves user data, and logs the user in.
    If the user does not exist, a new user is created.

    Args:
        request (HttpRequest): The HTTP request object containing the token.

    Returns:
        HttpResponse:   Redirects to the appropriate page based on user status.
                        Returns error responses for invalid tokens or request methods.
    """
    if request.method == 'POST':
        token = request.POST.get('credential')
        if not token:
            return HttpResponse('No token provided', status=400)

        try:
            # Verify the Google OAuth2 token
            user_data = id_token.verify_oauth2_token(
                token, google_requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
            )
        except ValueError:
            return HttpResponse('Invalid token', status=403)

        # Extract user information from the token
        email = user_data.get('email')
        name = user_data.get('name', '')

        # Split the name into first and last name components
        name_parts = name.split(' ')
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Create or get the user and log them in
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'email': email}
        )

        login(request, user)

        # Store user data in the session
        request.session['user_data'] = {
            'email': email,
            'name': f"{first_name} {last_name}"
        }

        # Redirect new users to select their role, existing users to the sign-in page
        if created:
            return redirect('users:select_role')
        else:
            return redirect('users:sign_in')

    return HttpResponse('Invalid request method', status=405)

@login_required
def select_role(request):
    """
    Handle role selection for authenticated users.

    Updates the user's profile with the selected role and renders the sign-in page
    with a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered page with a success message or an error response for invalid role selection.
    """
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        if selected_role in ['admin', 'user']:
            # Update the user's profile with the selected role
            request.user.profile.role = selected_role
            request.user.profile.save()

            # Ensure 'user_data' exists in the session before updating it
            if 'user_data' not in request.session:
                request.session['user_data'] = {}

            # Update the session with the selected role
            request.session['user_data']['role'] = selected_role

            # Create a success message based on the role
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

        return HttpResponse('Invalid role selection', status=400)

    return render(request, 'users/select_role.html')

def sign_out(request):
    """
    Log out the user and clear session data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the sign-in page after logging out the user.
    """
    request.session.pop('user_data', None)  # Safely remove 'user_data' if it exists
    logout(request)
    return redirect('users:sign_in')
