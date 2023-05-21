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

    def clean(self, request):
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)

        # Checks for when creating a new user note object.
        if request.method == 'POST':
            x = UserNote.objects.filter(
                owner=request.user, target_user=self.target_user).count()
            if x > 0:
                errors['non_field_errors'].append(
                    'Can only have one user note per other user.')

        if len(self.content) > 200:
            errors['content'].append('Max length is 200 characters.')

        # If any errors, raise ValidationError
        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.owner.username} - {self.target_user.username}'
