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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return JsonResponse(serializer.data, status="201")
        else:
            return JsonResponse(serializer.errors, status="400")

    def perform_create(self, serializer):
        try:
            serializer.save(owner_id=self.request.user.id)
        except Exception as err:
            print(err)


class LFGDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFGSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFG.objects.annotate(
    ).order_by('-id')
