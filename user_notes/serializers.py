from rest_framework import serializers
from user_notes.models import UserNote


class UserNoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate(self, data):
        instance = UserNote(**data)
        # Perform model's clean function
        request = self.context['request']
        instance.clean(request)
        return data

    class Meta:
        model = UserNote
        fields = [
            'id',
            'owner',
            'is_owner',
            'target_user',
            'content',
        ]
