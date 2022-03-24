from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from user.manager import CustomUserManager


def set_referal_code():
    return get_random_string(length=6)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(max_length=20, unique=True)
    referal_code = models.CharField(
        max_length=6, unique=True, default=set_referal_code, db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
