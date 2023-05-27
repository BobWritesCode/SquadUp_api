from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.core.files.images import get_image_dimensions


class Profile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    tracker = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='avatars/', default='default/awaiting_image_lcpknr'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-owner']

    def __str__(self):
        return f"{self.owner}'s profile"

    def clean(self, request):
        """
        Validates data being saved to Post model.
        - image file size: Cannot be over 2mb.
        - image height: Cannot be over 1080 pixels.

        Decorators:
            None
        Args:
            None
        Returns:
            None
        """
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)
        if self.image:
            max_size = 2 * 1024 * 1024  # 2MB
            max_height = 1080
            width, height = get_image_dimensions(self.image)
            # Check file size not too large.
            if self.image.size > max_size:
                errors['image'].append(
                    'The image file should not exceed 2MB.')
            # Check the height.
            if height > max_height:
                errors['image'].append(
                    'The image height cannot exceed 1080 pixels.')
        # If any above errors, raise ValidationError
        if errors:
            raise ValidationError(errors)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
