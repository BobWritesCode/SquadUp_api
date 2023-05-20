from rest_framework import generics, permissions, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly, IsGroupOwnerOrReadOnly
from .models import LFGSlotApply
from .serializers import LFGSlotApplySerializer
import bleach
from django.core.exceptions import ValidationError
from django.http import JsonResponse


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

    def perform_create(self, serializer):
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status="400")
        serializer.save(owner=self.request.user)


class LFGSlotApplyPagination(generics.ListAPIView):
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
            print(err)
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
