from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import LFG_Slot
from lfg_slots_apply.models import LFGSlotApply
from .serializers import LFG_SlotSerializer
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Q


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


class LFG_SlotReopen(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFG_SlotSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFG_Slot.objects.annotate().order_by('-id')

    def partial_update(self, request, *args, **kwargs):
        '''
        Reopen slot that was previously closed due to an accepted request.
        Delete all current slot requests for target slot.
        '''
        instance = self.get_object()
        # Crate a mutable copy of the request data
        mutable_data = request.POST.copy()
        mutable_data['status'] =  request.data.get('status', instance.status)
        serializer = self.get_serializer(
            instance, data=mutable_data, partial=True)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status="400")

        try:
            self.perform_update(serializer)
            # Delete all requests that exist current for this slot.
            query = Q(slot=instance.id)
            LFGSlotApply.objects.filter(query).delete()
            return JsonResponse({'post': serializer.data, }, status=200)

        except ValidationError as err:
            errorList = []
            for e in err:
                errorList.append(e[1])
            return JsonResponse({
                'non_field_errors': errorList,
            }, status=400)

        except Exception as err:
            return JsonResponse({
                'non_field_errors': ['Unknown error (African Elephant)'],
            }, status=400)
