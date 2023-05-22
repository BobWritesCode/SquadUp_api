from rest_framework import serializers
from lfg.models import LFG
from lfg_slots.models import LFG_Slot


class LFGSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.pk')
    is_owner = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_roles(self, obj):
        groups = LFG_Slot.objects.filter(lfg=obj.id)
        return [group.role for group in groups]

    def validate(self, data):
        instance = LFG(**data)
        # Perform model's clean function
        instance.clean()
        return data

    class Meta:
        model = LFG
        fields = [
            'id',
            'owner',
            'owner_id',
            'game_type',
            'max_team_size',
            'current_team_size',
            'lowest_rank',
            'highest_rank',
            'content',
            'is_owner',
            'status',
            'roles',
        ]
