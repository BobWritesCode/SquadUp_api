from rest_framework import generics, permissions, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly, IsGroupOwnerOrReadOnly
from .models import LFGSlotApply
from lfg_slots.models import LFG_Slot
from lfg.models import LFG
from .serializers import LFGSlotApplySerializer
import bleach
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q
from collections import defaultdict


class LFGSlotApplyList(generics.ListCreateAPIView):
    serializer_class = LFGSlotApplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFGSlotApply.objects.all().order_by('-id')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ['slot', 'owner', 'status']
    search_fields = ['slot', 'owner', 'status']
    ordering_fields = []

    def create(self, request, *args, **kwargs):
        query = Q(owner=self.request.user) & Q(status="Awaiting")
        try:

            if LFGSlotApply.objects.filter(query).count() == 5:
                errors = defaultdict(list)
                errors['non_field_errors'].append(
                    'You already have 5 open requests.')
                raise ValidationError(errors)

            slot = LFG_Slot.objects.get(pk=request.data['slot'])
            role = request.data['role']
            content = request.data['content']
            rank = request.data['rank']
            now_slot = LFGSlotApply.create(
                owner=request.user, slot=slot, role=role,
                content=content, rank=rank)
            now_slot.save()

        except ValidationError as err:
            errorList = []
            for e in err:
                errorList.append(e[1])
            return JsonResponse({
                'non_field_errors': errorList,
            }, status=400)

        else:
            return JsonResponse({
                'success': ['Posted'],
            }, status=200)


class LFGSlotApplyPagination(generics.ListAPIView):
    serializer_class = LFGSlotApplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LFGSlotApply.objects.all().order_by('-id')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ['id', 'slot', 'owner', 'status']
    search_fields = ['slot', 'owner', 'status']
    ordering_fields = []
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 1


class LFGSlotApplyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LFGSlotApplySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = LFGSlotApply.objects.annotate().order_by('-id')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Crate a mutable copy of the request data
        mutable_data = request.POST.copy()
        mutable_data['content'] = bleach.clean(
            request.data.get('content', instance.content))
        serializer = self.get_serializer(
            instance, data=mutable_data, partial=True)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status="400")

        try:
            self.perform_update(serializer)
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
                'non_field_errors': ['Unknown error (African Civet)'],
            }, status=400)


class LFGSlotUpdateDetail(generics.RetrieveUpdateAPIView):
    '''
    View class.

    Allows a group owner to view and updated a request application.
    '''
    serializer_class = LFGSlotApplySerializer
    permission_classes = [IsGroupOwnerOrReadOnly]
    queryset = LFGSlotApply.objects.annotate().order_by('-id')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Crate a mutable copy of the request data
        mutable_data = request.POST.copy()
        mutable_data['reply_content'] = bleach.clean(
            request.data.get('reply_content', instance.reply_content))
        serializer = self.get_serializer(
            instance, data=mutable_data, partial=True)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status="400")

        try:
            self.perform_update(serializer)

            if mutable_data['status'] == 'Accepted':
                # Change all awaiting requests for this slot to rejected.
                query = Q(status="Awaiting") & Q(
                    slot_id=instance.slot_id) & ~Q(pk=instance.pk)
                LFGSlotApply.objects.filter(query).update(status="Rejected")
                # Change status of slot to closed.
                LFG_Slot.objects.filter(
                    pk=instance.slot_id).update(status="Closed")

                # Check how many slots are still open, if 0 close group.
                lfg_slot = LFG_Slot.objects.get(pk=instance.slot_id)
                lfg_slots = LFG_Slot.objects.filter(
                    lfg=lfg_slot.lfg, status='Open')
                if lfg_slots.count() == 0:
                    LFG.objects.filter(pk=lfg_slot.lfg.id).update(status=False)
                    # Group now closed.

            return JsonResponse({'post': serializer.data, }, status=200)

        except ValidationError as err:
            errorList = []
            for e in err:
                errorList.append(e[1])
            return JsonResponse({
                'non_field_errors': errorList,
            }, status=400)

        except Exception as err:
            print(err)
            return JsonResponse({
                'non_field_errors': ['Unknown error (African Clawed Frog)'],
            }, status=400)
