from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import UserNote
from .serializers import UserNoteSerializer


class UserNoteList(generics.ListCreateAPIView):
    serializer_class = UserNoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserNote.objects.all().order_by('-id')
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


class UserNoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserNoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = UserNote.objects.annotate().order_by('-id')
