from django.db.models import Count
from rest_framework import generics, filters
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import Profiles
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profiles.objects.annotate().order_by('-username')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profiles.objects.annotate().order_by('-date_joined')
