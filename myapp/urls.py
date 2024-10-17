from django.urls import path
from . import views

app_name = 'myapp' # makes referencing urls easier

urlpatterns = [
    path('', views.home, name='home'),
    path('assignments/add/', views.add_assignment, name='add_assignment'),
]