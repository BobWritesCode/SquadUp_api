from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import UserNote
from .serializers import UserNoteSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        target_user = User.objects.get(pk=pk)
        query = Q(owner=request.user) & Q(target_user=target_user)
        user_note = UserNote.objects.filter(query).first()
        # If note object exists, return contents.
        if user_note:
            return JsonResponse({
                'user_note': [user_note.content],
            }, status=200)
        # If note object does not exists, return blanks string.
        return JsonResponse({
            'user_note': [''],
        }, status=200)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data['content'] = bleach.clean(
            request.data.get('content', instance.content))
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
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
                'non_field_errors': ['Unknown error (African buffalo)'],
            }, status=400)
