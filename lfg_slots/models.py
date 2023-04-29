from django.db import models
from django.contrib.auth.models import User
from lfg.models import LFG


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
    Lfg = models.ForeignKey(LFG, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, blank=False, default='Any')
    status = models.CharField(choices=STATUS_CHOICES, max_length=6, blank=False, default='Open')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} - {self.role}'