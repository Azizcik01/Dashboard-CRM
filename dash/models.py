from typing import Any
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from methodism.models import Otp
# Create your models here.


class Employer(models.Model):
    ism = models.CharField(max_length=128)
    yosh = models.IntegerField(default=0)
    lavozim = models.CharField(max_length=128)
    maosh = models.IntegerField(default=0)
    maosh_type = models.CharField(max_length=3, choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('RUB', 'RUB'),
    ])

    def __str__(self) -> str:
        return self.ism
    

class CustomManager(UserManager):

    def create_user(self, username, email, password=None, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self.create_user(username=username, email=email, password=password, is_staff=True, is_superuser=True)
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    fio = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class OtpToken(Otp):
    email = models.EmailField()

