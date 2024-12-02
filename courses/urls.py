from django.urls import path
from . import views

app_name = 'courses' 

urlpatterns = [
    # Course management
    path('course/create/', views.create_course_group, name='create_course'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/edit/', views.edit_course_description, name='edit_course_description'),
    
    # Enrollment management
    path('course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('course/<int:course_id>/unenroll/', views.unenroll_from_course, name='unenroll_from_course'),
    
    # Enrollment request management
    path('course/<int:course_id>/request-enrollment/', views.request_enrollment, name='request_enrollment'),
    path('enrollment-request/<int:request_id>/<str:action>/', views.manage_enrollment_request, name='manage_enrollment_request'),
    path('courses/admin/', views.admin_course, name='admin_course'),
]