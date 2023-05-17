from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import LFG_Slot
from .serializers import LFG_SlotSerializer


class LFG_SlotList(generics.ListCreateAPIView):
    serializer_class = LFG_SlotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFG_Slot.objects.all().order_by('-id')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['lfg']
    search_fields = ['owner']
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LFG_SlotDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFG_SlotSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFG_Slot.objects.annotate().order_by('-id')
