from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import LFGSlotApply
from .serializers import LFGSlotApplySerializer


class LFGSlotApplyList(generics.ListCreateAPIView):
    serializer_class = LFGSlotApplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFGSlotApply.objects.all().order_by('-id')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ['slot', 'owner']
    search_fields = ['slot', 'owner']
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LFGSlotApplyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFGSlotApplySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFGSlotApply.objects.annotate().order_by('-id')
