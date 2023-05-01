from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from lfg_slots_apply.models import LFGSlotApply


class LFGSlotApplySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = LFGSlotApply
        fields = [
            'id',
            'slot',
            'role',
            'rank',
            'content',
            'created_at',
            'owner',
            'is_owner',
            'status',
        ]
