from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, password, email, **extra_fields):

        if not password:
            raise ValueError('password must be value')

        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            raise ValueError("'email' is empty")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_staff(self, password, email=None, username=None, **extra_fields):
        user = self.create_user(
            password=password,
            email=email,
            username=username,
            **extra_fields
        )
        user.is_staff = True
        user.is_user = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, default=str(), blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=10, default=None, blank=True, null=True)
    phone = models.CharField(max_length=20, default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    customer_xid = models.UUIDField(unique=True, db_index=True, auto_created=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    @property
    def phone_with_code(self):
        number = ''
        if self.phone and self.country_code:
            number = self.country_code + self.phone

        elif self.phone and not self.country_code:
            number = '+91' + self.phone
        return number
