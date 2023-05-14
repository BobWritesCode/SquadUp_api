import re
from rest_framework import generics, filters
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from cloudinary import uploader
import urllib.parse

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate().order_by('-owner')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate().order_by('-owner')

    def put(self, request, *args, **kwargs):

        user = User.objects.get(pk=request.user.id)
        profile = get_object_or_404(Profile, owner=user)
        serializer = self.serializer_class(profile, data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data.get('image')
            tracker = serializer.validated_data.get('tracker')

            if tracker:
                s = urllib.parse.quote_plus(tracker, safe='')
                serializer.validated_data['tracker'] = str(s)
                serializer.save()
                return JsonResponse({
                    'tracker': ['Tracker updated.'],
                    'response': [s],
                }, status=200)

            if image:
                if profile.image is not None and request.FILES:
                    # Delete old image from Cloudinary server
                    try:
                        uploader.destroy(str(profile.image))
                    except:
                        pass

                if request.FILES:
                    # Upload new image
                    new_image = uploader.upload(
                        request.FILES['image'],
                        folder="squadup/avatars/",
                        allowed_formats=['jpg', 'png', 'jpeg'],
                        format='jpg'
                    )
                    serializer.validated_data['image'] = new_image['public_id']
                    serializer.save()
                    return JsonResponse({
                        'success': ['Avatar updated successfully.'],
                        'url': [new_image['url']],
                    }, status=200)

            return JsonResponse({
                'non_field_errors': ['Form is missing information.'],
            }, status=400)


@csrf_exempt
def user_email(request: object, user_id: int = None):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist.'}, status=404)

    if request.method == 'PUT':
        email = request.body.decode('utf-8')

        result = check_email(email.lower())
        if not result:
            return JsonResponse({
                'email': ['Email address not valid.']
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email': ['A user with that email already exists.']
            }, status=400)
        else:
            user.email = email
            user.save()
            return JsonResponse({'message': 'Email address updated successfully.'}, status=200)

    if request.method == 'GET':
        return JsonResponse({
            'email': user.email,
        }, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def check_email(email: str):
    """
    Checks email address given conforms to rules.

    Args:
        email (string): Username given.

    Returns:
        {result (bool)}
    """
    pat = (
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#"
        "#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9"
        r"-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    if re.match(pat, email) is None:
        return False
    return True

