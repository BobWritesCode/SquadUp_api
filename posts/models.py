from django.db import models
from django.contrib.auth.models import User
import bleach
from django.core.exceptions import ValidationError


class Post(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='post_images/', blank=True
    )

    @classmethod
    def create(cls, owner, content : str = '' , image = None):
        post = cls(owner=owner, content=content, image=image)
        return post

    def clean(self):
        """
        Validates data being saved to Post model.
        - content: max_length = 400
        - content & image : Cannot both be blank.

        Decorators:
            None
        Args:
            None
        Returns:
            None
        """
        # Remove whitespaces at beginning and end of string.
        self.content.strip()
        self.content = bleach.clean(self.content)
        if len(self.content) > 400:
            raise ValidationError(
                {'content' : 'Max length is 400 characters.'}
                )
        if not self.content and not self.image:
            raise ValidationError(
                {'non_field_errors' : 'Cannot be blank: Must provide text or image.'}
                )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
