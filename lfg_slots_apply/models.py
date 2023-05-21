from django.db import models
from django.contrib.auth.models import User
from lfg_slots.models import LFG_Slot
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db.models import Q

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
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)


class LFGSlotApply(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(LFG_Slot, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=10, blank=False, default='Any')
    rank = models.CharField(choices=RANK_CHOICES,
                            max_length=9, blank=False, default='0')
    content = models.TextField(blank=True, max_length=100)
    reply_content = models.TextField(blank=True, max_length=100)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=8, blank=False, default='Awaiting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} - {self.role}'

    def clean(self, request):
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)
        query = Q(owner=request.user) & Q(status="Awaiting")
        if LFGSlotApply.objects.filter(query).count() == 5:
            errors['non_field_errors'].append(
                'You already have 5 open requests.')
        if len(self.content) > 100:
            errors['content'].append('Max length is 100 characters.')

        # This checks are only needed if request is being accepted.
        if self.status == "Accepted":
            if len(self.reply_content) > 100:
                errors['reply_content'].append('Max length is 100 characters.')
            if len(self.reply_content) < 10:
                errors['reply_content'].append(
                'You should provide some instructions so the person can join your team. (minimum of 10 characters)')

        # If any above errors, raise ValidationError
        if errors:
            raise ValidationError(errors)
