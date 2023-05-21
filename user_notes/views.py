from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import UserNote
from .serializers import UserNoteSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
import bleach
from django.core.exceptions import ValidationError


class UserNoteList(generics.ListCreateAPIView):
    serializer_class = UserNoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserNote.objects.all().order_by('-id')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner', 'target_user',
    ]
    search_fields = [
        'owner', 'target_user',
    ]
    ordering_fields = [
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserNoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserNoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = UserNote.objects.annotate().order_by('-id')

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
            return JsonResponse(serializer.data, status=200)

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
                'non_field_errors': ['Unknown error (African Buffalo)'],
            }, status=400)
