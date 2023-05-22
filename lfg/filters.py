from django_filters.rest_framework import FilterSet, NumberFilter
from .models import LFG
from django_filters import CharFilter


class LFGListFilter(FilterSet):
    lowest_rank__gte = NumberFilter(
        field_name='lowest_rank', lookup_expr='gte')
    lowest_rank__lte = NumberFilter(
        field_name='lowest_rank', lookup_expr='lte')
    highest_rank__gte = NumberFilter(
        field_name='highest_rank', lookup_expr='gte')
    highest_rank__lte = NumberFilter(
        field_name='highest_rank', lookup_expr='lte')
    role = CharFilter(field_name='lfg_slot__role', lookup_expr='contains')

    class Meta:
        model = LFG
        fields = ['owner', 'status', 'game_type',
                  'lowest_rank', 'highest_rank', 'role']
