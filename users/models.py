#
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
import random

from django.utils import timezone

created_at = models.DateTimeField(default=timezone.now, auto_now_add=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()

#
# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#
#     groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
#
