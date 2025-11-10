from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

def avatar_upload_path(instance, filename):
    return f"avatars/user_{instance.user_id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    # Ya existente (lo conservamos)
    display_name = models.CharField(max_length=60, blank=True)

    # Campos típicos que suelen venir desde la app móvil (todos opcionales)
    phone            = models.CharField(max_length=30, blank=True)
    gamer_tag        = models.CharField(max_length=60, blank=True)
    favorite_platform= models.CharField(max_length=40, blank=True)   # "PlayStation", "Xbox", etc.
    birth_date       = models.DateField(blank=True, null=True)

    # Dirección
    street           = models.CharField(max_length=200, blank=True)
    district         = models.CharField(max_length=120, blank=True)  # colonia
    city             = models.CharField(max_length=120, blank=True)
    state            = models.CharField(max_length=120, blank=True)
    zipcode          = models.CharField(max_length=10, blank=True)

    # Preferencias
    newsletter_ok    = models.BooleanField(default=False)
    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def name_for_display(self):
        return self.display_name or self.user.get_full_name() or self.user.username

# Auto-crear perfil
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
