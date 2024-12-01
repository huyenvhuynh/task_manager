from django.contrib import admin
from .models import Course, EnrollmentRequest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course_name', 'course_number', 'creator', 'privacy')
    search_fields = ('course_name', 'course_number', 'creator__username', 'description')
    list_filter = ('privacy', 'creator')
    readonly_fields = ('full_name',)
    filter_horizontal = ('enrolled_users',)
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_name', 'course_number', 'full_name', 'description')
        }),
        ('Access Settings', {
            'fields': ('privacy', 'creator', 'enrolled_users')
        }),
    )

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'request_date', 'response_date')
    list_filter = ('status', 'request_date', 'response_date')
    search_fields = ('user__username', 'course__course_name')
    readonly_fields = ('request_date',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'course', 'status')
        }),
        ('Dates', {
            'fields': ('request_date', 'response_date')
        }),
    )