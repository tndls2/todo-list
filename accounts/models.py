from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from core.utils.model import TimestampZone


class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        """
        Create and return a regular user with a username and password.
        """
        if not user_name:
            raise ValueError('The User must have a user_name.')
        if self.filter(user_name=user_name).exists():  # user_name 중복 체크
            raise ValueError('A user with this user_name already exists.')

        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        """
        Create and return a superuser with a username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_name, password, **extra_fields)


class User(TimestampZone):
    # Django 내장 User 모델 및 기능을 사용하지 않고 직접 구현
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(_("password"), max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.user_name

    def set_password(self, raw_password):
        """
        Set the password for this user. The raw password is hashed and stored in the database.
        """
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """
        Check if the raw_password matches the hashed password stored in the database.
        """
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """
        Save the user instance, ensuring the password is properly hashed.
        """
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Check if the user has any permissions in a given app.
        """
        return self.is_superuser

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True