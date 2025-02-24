from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update a user profile when a User instance is saved.

    This signal handler ensures that a Profile instance is created for newly created
    User instances and updated for existing User instances if necessary.

    Args:
        sender (Model): The model class that sends the signal (User).
        instance (User): The instance of the model being saved.
        created (bool): True if a new record was created, False if an existing record was updated.
        **kwargs: Additional keyword arguments.

    Side Effects:
        - Creates a new Profile instance for newly created User instances.
        - Updates or creates a Profile instance for existing User instances that lack one.

    """
    if created:
        # Create a profile for new users
        Profile.objects.create(user=instance, role='user')
    else:
        # Check if the user has a profile; if not, create one
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance, role='user')
        else:
            instance.profile.save()
