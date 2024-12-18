from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserSettings

# Define el manejador de señales para crear un UserSettings cuando se guarda un User
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)

# Conecta el manejador de señales
post_save.connect(create_user_settings, sender=User)
