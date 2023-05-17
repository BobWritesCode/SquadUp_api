from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from lfg_slots.models import LFG_Slot


class LFG_SlotSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = LFG_Slot
        fields = [
            'id',
            'lfg',
            'role',
            'status',
            'content',
            'created_at',
            'content',
            'owner',
            'is_owner',
        ]
