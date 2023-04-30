from rest_framework import serializers
from lfg_slots.models import LFG_Slot


class LFG_SlotSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = LFG_Slot
        fields = [
            'id',
            'Lfg',
            'role',
            'status',
            'content',
            'created_at',
            'content',
            'owner',
            'is_owner',
        ]
