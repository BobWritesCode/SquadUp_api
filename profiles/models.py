from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profiles(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    tracker = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='images/', default='squad_up/default_profile_n8u8ru'
    )

    class Meta:
        ordering = ['-owner']

    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
