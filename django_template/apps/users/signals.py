from .models import UserSettings
from django.dispatch import receiver
from social.models import CommonProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile_and_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
        CommonProfile.objects.create(user_common=instance)