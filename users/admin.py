from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Profile model in the Django admin interface.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields that can be searched in the admin interface.
        list_filter (tuple): Fields to filter by in the admin list view.
    """
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role')
    list_filter = ('role',)

# Register the Profile model with the customized admin class
admin.site.register(Profile, ProfileAdmin)
