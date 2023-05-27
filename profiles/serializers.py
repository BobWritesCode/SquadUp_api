from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    email = serializers.ReadOnlyField(source='owner.email')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate(self, data):
        instance = Profile(**data)
        # Perform model's clean function
        instance.clean(self.context['request'])
        return data

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'tracker',
            'image',
            'created_at',
            'is_owner',
            'email',
        ]
