from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from collections import defaultdict

GAME_TYPE_CHOICES = (
    ('1', 'Competitive'),
    ('2', 'Tournament'),
    ('3', 'Casual'),
)

RANK_CHOICES = (
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


class LFG(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(
        choices=GAME_TYPE_CHOICES, max_length=11, blank=False, default='Competitive')
    max_team_size = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)], blank=False)
    current_team_size = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)], blank=False)
    lowest_rank = models.CharField(
        choices=RANK_CHOICES, max_length=9, blank=False, default='Iron')
    highest_rank = models.CharField(
        choices=RANK_CHOICES, max_length=9, blank=False, default='Iron')
    content = models.TextField(blank=True, max_length=200)

    class Meta:
        ordering = ['-id']

    def clean(self):
        # defaultdict auto creates key first time it is accessed.
        errors = defaultdict(list)
        # Check current team size is smaller then man team size.
        if self.current_team_size >= self.max_team_size:
            errors["current_team_size"].append('Current team size must be smaller then max team size.')
        # Check min rank is lower than max rank.
        if self.lowest_rank >= self.highest_rank:
            errors["highest_rank"].append('Maximum rank must be same or higher than minimum rank.')
        # If any errors, raise ValidationError
        if errors:
            raise ValidationError(errors)


    def __str__(self):
        return f'{self.id} - {self.owner.username} - {self.game_type}'
