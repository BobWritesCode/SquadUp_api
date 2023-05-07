from django.db import models
from django.contrib.auth.models import User

class UserNote(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user')
    content = models.TextField(blank=True, max_length=200)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.owner.username} - {self.target_user.username}'
