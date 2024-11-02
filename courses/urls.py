from django.urls import path
from . import views

app_name = 'courses' 

urlpatterns = [
    path('course/create/', views.create_course_group, name='create_course'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/', views.course_list, name='course_list'),  # To see all courses
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
]