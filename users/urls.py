from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    path('google-sign-in/', views.google_sign_in, name='google_sign_in'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('auth-receiver/', views.auth_receiver, name='auth_receiver'),
    path('select-role/', views.select_role, name='select_role'),

]