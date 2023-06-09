from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import LFG
from lfg_slots.models import LFG_Slot
from .serializers import LFGSerializer
from django.http import JsonResponse
import json
from django.core import serializers
from .filters import LFGListFilter


class LFGList(generics.ListCreateAPIView):
    serializer_class = LFGSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFG.objects.all().order_by('-id')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # Replace filterset_fields with filterset_class
    filterset_class = LFGListFilter
    search_fields = [
        'owner', 'status', 'game_type'
    ]
    ordering_fields = [
    ]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # Organise data sent from API
        formData = data['formData']
        slots = data['slots']
        serializer = self.get_serializer(data=formData)
        # Validate data, if any errors feedback to frontend.
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status="400")
        # Create LFG and add to database.
        self.perform_create(serializer)
        # Get Lfg instance.
        instance = serializer.instance
        # Create slots and add to database
        for slot in slots:
            slot = LFG_Slot.create(
                owner=request.user, lfg=instance, role=slot['role'],
                content=slot['content'])
            slot.save()
        # Feedback status 200 if all okay.
        return JsonResponse({
            "slot_id": instance.pk,
            "status": "OK"
        }, status="201")

    def perform_create(self, serializer):
        try:
            serializer.save(owner_id=self.request.user.id)
        except Exception as err:
            print(err)


class LFGDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFGSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFG.objects.annotate().order_by('-id')
