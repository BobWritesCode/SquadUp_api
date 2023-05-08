from rest_framework import generics, permissions
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

    def put(self, request, *args, **kwargs):
        # Use Bleach to remove malicious script tags
        new_note = bleach.clean(request.data['userNote'])
        # Get target user profile PK
        pk = self.kwargs.get('pk')
        # Search for user note object, if exists.
        query = Q(owner=request.user.id) & Q(target_user=pk)
        user_note = UserNote.objects.filter(query).first()
        # If a user note object already exists, proceed to edit object.
        if user_note:
            user_note = get_object_or_404(UserNote, query)
            user_note.content = new_note
            try:
                # Run clean method to check for errors.
                user_note.clean()
                # Update object.
                user_note.save()

            except ValidationError as err:
                errorList = []
                for e in err:
                    errorList.append(e[1])
                return JsonResponse({
                    'non_field_errors': errorList,
                }, status=400)

            # Unexpected error has occurred and unique error code.
            except Exception as err:
                return JsonResponse({
                    'non_field_errors': ['Unknown error (Aardwolf)'],
                }, status=400)

            # If no errors return saved string.
            return JsonResponse({
                'user_note': [new_note],
            }, status=200)

        # If user note object does not exist then create obj.
        if not user_note:
            target_user = User.objects.get(pk=pk)
            try:
                # Create instance of UserNote.
                newUserNote = UserNote.create(request.user, target_user, new_note)
                # Run clean method to check for errors.
                newUserNote.clean()
                # Save instance as object.
                newUserNote.save()
            except ValidationError as err:
                errorList = []
                for e in err:
                    errorList.append(e[1])
                return JsonResponse({
                    'non_field_errors': errorList,
                }, status=400)
            # Unexpected error has occurred and unique error code.
            except Exception as err:
                return JsonResponse({
                    'non_field_errors': ['Unknown error (Adelie Penguin)'],
                }, status=400)

            return JsonResponse({
                'user_note': [new_note],
                'response': ['Created new note.'],
            }, status=200)

        return JsonResponse({
            'non_field_errors': ['Unknown error (Abyssinian Cat)'],
        }, status=400)
