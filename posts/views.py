from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from cloudinary import uploader
from django.core import serializers

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
    ]
    ordering_fields = [
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        """
        Returns a specific post by ID.

        Decorators:
            None
        Args:
            None
        Returns:
            JsonResponse - Post to return.
        """
        pk = self.kwargs.get('pk')
        try:
            queryset = Post.objects.get(pk=pk)
            # Check if image exists in obj, is so only return URL,
            # if not return blank string.
            if queryset.image:
                url = queryset.image.url
            else:
                url = ''
            return JsonResponse({
                'success': [''],
                'post': serializers.serialize('json', [ queryset, ]),
                'imageURL': url,
            }, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({
                'non_field_errors': [err],
            }, status=400)


    def put(self, request, *args, **kwargs):
        """
        Creates new post object from API request.

        Decorators:
            None
        Args:
            None
        Returns:
            JsonResponse - Response provides feedback to request.
        """
        image = None
        if request.FILES:
            # Upload new image to cloudinary.
            new_image = uploader.upload(
                request.FILES['image'],
                folder="squadup/post_images/",
                allowed_formats=['jpg', 'png', 'jpeg'],
                format='jpg'
            )
            image = new_image['public_id']
        try:
            content = request.data['content']
            new_post = Post.create(
                owner=request.user, content=content, image=image)
            new_post.clean()
            new_post.save()
        except ValidationError as err:
            errorList = []
            for e in err:
                errorList.append(e[1])
            return JsonResponse({
                'non_field_errors': errorList,
            }, status=400)
        except Exception as err:
            return JsonResponse({
                'non_field_errors': ['Unknown error (Afghan Hound)'],
            }, status=400)
        else:
            return JsonResponse({
                'success': ['Posted'],
                'postID': new_post.pk,
            }, status=200)
