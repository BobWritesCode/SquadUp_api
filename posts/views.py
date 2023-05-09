from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from cloudinary import uploader


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
    queryset = Post.objects.annotate(
    ).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        print('get')

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
            # Upload new image
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
            }, status=200)
