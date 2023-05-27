from django.db import models
from django.contrib.auth.models import User
import bleach
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.core.files.images import get_image_dimensions


class Post(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='post_images/', blank=True
    )

    @classmethod
    def create(cls, owner, content: str = '', image=None):
        post = cls(owner=owner, content=content, image=image)
        return post

    def clean(self):
        """
        Validates data being saved to Post model.
        - content: max_length = 400 characters.
        - content & image : Cannot both be blank.
        - image file size: Cannot be over 2mb.
        - image height: Cannot be over 1000 pixels.

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
            max_height = 1000
            width, height = get_image_dimensions(self.image)
            # Check file size not too large.
            if self.image.size > max_size:
                errors['image'].append(
                    'The image file should not exceed 2MB.')
            # Check the height.
            if height > max_height:
                errors['image'].append(
                    'The image height cannot exceed 1000 pixels.')
        # Remove whitespaces at beginning and end of string.
        self.content.strip()
        # Remove any malicious html tags.
        self.content = bleach.clean(self.content)
        if len(self.content) > 400:
            errors['content'].append(
                'Max length is 400 characters.')
        if not self.content and not self.image:
            errors['non_field_errors'].append(
                'Cannot be blank: Must provide text or image.')
        # If any above errors, raise ValidationError
        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.owner}'
