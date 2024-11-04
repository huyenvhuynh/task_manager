from django.urls import path
from . import views

app_name = 'myapp' # makes referencing urls easier

urlpatterns = [
    path('', views.home, name='home'),
    path('assignments/add/', views.add_assignment, name='add_assignment'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('file_search/', views.file_search, name='file_search'),
    path('calender/', views.calender, name='calender'),
]