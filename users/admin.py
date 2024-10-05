from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role')
    list_filter = ('role',)

admin.site.register(Profile, ProfileAdmin)