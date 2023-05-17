from django.db import models
from django.contrib.auth.models import User
from lfg_slots.models import LFG_Slot

ROLE_CHOICES = (
    ('Any', 'Any'),
    ('Duelist', 'Duelist'),
    ('Initiator', 'Initiator'),
    ('Controller', 'Controller'),
    ('Sentinel', 'Sentinel'),
)

RANK_CHOICES = (
    ('0', 'Unranked'),
    ('1', 'Iron'),
    ('2', 'Bronze'),
    ('3', 'Silver'),
    ('4', 'Gold'),
    ('5', 'Platinum'),
    ('6', 'Diamond'),
    ('7', 'Ascendant'),
    ('8', 'Immortal'),
    ('9', 'Radiant'),
)

STATUS_CHOICES = (
    ('Awaiting', 'Awaiting'),
    ('Accept', 'Accept'),
    ('Reject', 'Reject'),
)


class LFGSlotApply(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(LFG_Slot, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=10, blank=False, default='Any')
    rank = models.CharField(choices=RANK_CHOICES,
                            max_length=9, blank=False, default='0')
    content = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=8, blank=False, default='Awaiting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} - {self.role}'
