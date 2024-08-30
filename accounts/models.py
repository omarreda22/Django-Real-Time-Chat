from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UsersManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have an username address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        # if len(password) < 8:
        #     raise ValueError("Password must be bigger than 8 Char")

        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=225, unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    avatar = models.ImageField(upload_to="users/avatar/", null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UsersManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email

    def full_name(self):
        return f"{self.first_name} {self.last_name}".title()
