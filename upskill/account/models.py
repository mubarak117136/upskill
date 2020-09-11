from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from .utils import *


# user profile manager
class UserProfileManager(BaseUserManager):
    """CUSTOM USER MANAGER"""

    def create_user(self, phone=None, password=None, **kwargs):

        user = self.model(phone=phone, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, phone, password, **kwargs):

        user = self.create_user(phone=phone, password=password, **kwargs)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# user profile model
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    join_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ("name", "email", )

    def __str__(self):
        if self.name:
            return self.name
        elif self.email:
            return self.email
        else:
            return self.phone
    

#login with phone or email
class PhoneOrEmailModelBackend(object):
    def authenticate(self, username=None, password=None):
        if check_bd_phone_number(username):
            kwargs = {'phone': username}
        else:
            kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None