from django.db import models
# from django.contrib.auth.models import User as django_user
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    ADMIN = 0
    MANAGER = 1
    SELLER = 2
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (SELLER, 'Seller'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

    branch = models.OneToOneField(
        "Branch",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_query_name='%(class)s',
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    # extra data

    salary = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    national_id = models.CharField(max_length=14, null=True, blank=True)


# class Seller(models.Model):
#     user_obj = models.OneToOneField(django_user, on_delete=models.CASCADE)
#     salary = models.PositiveIntegerField(null=True, blank=True)
#     phone_number = models.CharField(max_length=11, null=True, blank=True)
#     age = models.PositiveIntegerField(null=True, blank=True)
#     national_id = models.CharField(max_length=14, null=True, blank=True)
#     manager = models.BooleanField(default=False)
#     branch = models.ForeignKey("Branch", on_delete = models.CASCADE)
#
#     def __str__(self):
#         return self.user_obj.username


class Branch(models.Model):
    name = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250, null=False, blank=True)
    phone_branch = models.CharField(max_length=11, null=False, blank=True)

    def __str__(self):
        return self.name