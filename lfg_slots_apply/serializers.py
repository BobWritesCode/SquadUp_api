from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from lfg_slots_apply.models import LFGSlotApply


class LFGSlotApplySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ownerID = serializers.ReadOnlyField(source='owner.id')
    is_owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate(self, data):
        instance = LFGSlotApply(**data)
        # Perform model's clean function
        instance.clean(self.context['request'])
        return data

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
            'ownerID',
            'is_owner',
            'status',
        ]
