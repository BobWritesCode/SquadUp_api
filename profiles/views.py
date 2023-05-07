import re
from django.db.models import Count
from rest_framework import generics, filters
from squadup_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

