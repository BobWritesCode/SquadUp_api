from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from collections import defaultdict


class UserNote(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='target_user')
    content = models.CharField(
        blank=True,
        max_length=200,
        error_messages={
            'max_length': "Max length is 200 character",
        })

    @classmethod
    def create(cls, owner, target_user, content):
        user_note = cls(owner=owner, target_user=target_user, content=content)
        return user_note

    def clean(self):
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)
        if len(self.content) > 200:
            errors['content'].append('Max length is 200 characters.')
        # If any errors, raise ValidationError
        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.owner.username} - {self.target_user.username}'
