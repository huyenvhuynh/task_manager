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
    return render(request, 'users/sign_in.html', {
        'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    })
    
def home(request):
    if request.user.is_authenticated:
        return render(request, 'users/home.html')
    else:
        return redirect('sign_in')

def sign_in(request):
    if request.user.is_authenticated:
        # User is already authenticated, show the success message
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
        # User is not authenticated, show the sign-in page
        context = {
            'google_client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        }
    
    return render(request, 'users/sign_in.html', context)



@csrf_exempt
def auth_receiver(request):
    if request.method == 'POST':
        token = request.POST.get('credential')
        if not token:
            return HttpResponse('No token provided', status=400)

        try:
            user_data = id_token.verify_oauth2_token(
                token, google_requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
            )
        except ValueError:
            return HttpResponse('Invalid token', status=403)

        email = user_data.get('email')
        name = user_data.get('name', '')

        name_parts = name.split(' ')
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        user, created = User.objects.get_or_create(
            username=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'email': email}
        )

        login(request, user)

        request.session['user_data'] = {
            'email': email,
            'name': f"{first_name} {last_name}"
        }

        if created:
            return redirect('select_role')
        else:
            return redirect('sign_in')  # Redirect to sign_in view for both new and returning users

    return HttpResponse('Invalid request method', status=405)


@login_required
def select_role(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        if selected_role in ['admin', 'user']:
            request.user.profile.role = selected_role
            request.user.profile.save()

            request.session['user_data']['role'] = selected_role

            if selected_role == 'admin':
                message = "Successfully signed in as an Administrator!"
            else:
                message = "Successfully signed in as a Common User!"

            return render(request, 'users/sign_in.html', {
                'message': message,
                'email': request.user.email,
                'name': request.user.get_full_name(),
            })

        return HttpResponse('Invalid role selection', status=400)

    return render(request, 'users/select_role.html')


def sign_out(request):
    del request.session['user_data']  
    logout(request)  
    return redirect('sign_in')
