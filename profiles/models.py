from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Profiles(AbstractUser):

    username = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        error_messages={
            'required': "Username is required. (Panda)",
            'unique': 'Username already taken. (Panda)'})
    username_lower = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            'required': "Email is required. (Cobra)",
            'unique': 'Email already taken. (Cobra)'})
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    tracker = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='images/', default='squad_up/default_profile_n8u8ru'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
        ordering = ['-date_joined']

    def __str__(self):
        return (f'PK: {self.id} - id: {self.id} - email: {self.email} '
                f'- username: {self.username}')

    def save(self, *args, **kwargs):
        # Convert email address to lowercase to stop duplication.
        self.email = str(self.email).lower()
        # Convert username to lowercase to stop duplication.
        self.username_lower = str(self.username).lower()

        if not self.pk:
            # Adding a new object.
            existing_usernames = Profiles.objects.filter(
                username_lower=self.username_lower)
            existing_emails = Profiles.objects.filter(
                email=self.email)
        else:
            # Updating an existing object.
            existing_usernames = Profiles.objects.filter(
                username_lower=self.username_lower).exclude(pk=self.pk)
            existing_emails = Profiles.objects.filter(
                email=self.email).exclude(pk=self.pk)

        errors = {}
        # No space in username.
        if ' ' in self.username_lower:
            errors['username'] = ['No spaces allowed. (Anaconda)']
        # No duplicate email addresses.
        if existing_emails:
            errors['email'] = ['Email already taken. (Jackal)']
        # No duplicate usernames.
        if existing_usernames:
            errors['username'] = ['Username already taken. (Lion)']
        # If any errors raise ValidationError.
        if errors:
            raise ValidationError(errors)

        super().save(*args, **kwargs)
