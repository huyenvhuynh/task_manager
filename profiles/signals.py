from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile for new users
        Profile.objects.create(user=instance, role='user')
    else:
        # Check if the user has a profile; if not, create one
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance, role='user')
        else:
            instance.profile.save()