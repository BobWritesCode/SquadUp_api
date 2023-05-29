from django.db import models
from django.contrib.auth.models import User
from lfg.models import LFG
from django.core.exceptions import ValidationError
from collections import defaultdict

ROLE_CHOICES = (
    ('Any', 'Any'),
    ('Duelist', 'Duelist'),
    ('Initiator', 'Initiator'),
    ('Controller', 'Controller'),
    ('Sentinel', 'Sentinel'),
)

STATUS_CHOICES = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)


class LFG_Slot(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    lfg = models.ForeignKey(LFG, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=10, blank=False, default='Any')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=6, blank=False, default='Open')
    content = models.TextField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} - {self.role}'

    @classmethod
    def create(cls, owner, lfg, role='Any', content='', status='Open'):
        slot = cls(owner=owner, lfg=lfg, role=role,
                   content=content, status=status)
        return slot

    def clean(self, request):
        """
        Validates data being saved.
        - content: max_length = 100 characters.

        Decorators:
            None
        Args:
            None
        Returns:
            None
        """
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)
        if len(self.content) > 100:
            errors['content'].append(
                'Max length is 100 characters.')
        # If any above errors, raise ValidationError
        if errors:
            raise ValidationError(errors)
