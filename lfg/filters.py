from django_filters.rest_framework import FilterSet, NumberFilter
from .models import LFG


class LFGListFilter(FilterSet):
    lowest_rank__gte = NumberFilter(
        field_name='lowest_rank', lookup_expr='gte')
    lowest_rank__lte = NumberFilter(
        field_name='lowest_rank', lookup_expr='lte')
    highest_rank__gte = NumberFilter(
        field_name='highest_rank', lookup_expr='gte')
    highest_rank__lte = NumberFilter(
        field_name='highest_rank', lookup_expr='lte')

    class Meta:
        model = LFG
        fields = ['owner', 'status', 'game_type',
                  'lowest_rank', 'highest_rank']
