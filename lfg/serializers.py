from rest_framework import serializers
from lfg.models import LFG


class LFGSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

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
            'game_type',
            'max_team_size',
            'current_team_size',
            'lowest_rank',
            'highest_rank',
            'content',
            'is_owner',
            'status',
        ]
