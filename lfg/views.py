from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import LFG
from .serializers import LFGSerializer


class LFGList(generics.ListCreateAPIView):
    serializer_class = LFGSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFG.objects.all().order_by('-id')
    filter_backends = [
    ]
    filterset_fields = [
    ]
    search_fields = [
    ]
    ordering_fields = [
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LFGDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFGSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFG.objects.annotate(
    ).order_by('-id')
