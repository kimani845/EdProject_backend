# Django signals allow certain senders to notify a set of receivers (functions) when some action has taken place.

# For example:

# After a user is created

# Before a model is saved

# After a model is deleted

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User, TutorProfile, StudentProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "tutor":
            TutorProfile.objects.create(user=instance)
        elif instance.role == "student":
            StudentProfile.objects.create(user=instance)