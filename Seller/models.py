from django.db import models
from django.contrib.auth.models import User as Django_User, UserManager, BaseUserManager, AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250, null=False, blank=True)
    phone_branch = models.CharField(max_length=11, null=False, blank=True)

    def __str__(self):
        return self.name

class Site_User(Django_User):

    USER_TYPE_CHOICES_Second = (
        (1, 'Manager'),
        (2, 'Seller'),
    )

    USER_TYPE_CHOICES = (
        (0, 'Admin'),
        (1, 'Manager'),
        (2, 'Seller'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    # Extra Data
    salary = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    national_id = models.CharField(max_length=14, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user_type != 0:
            self.is_staff = False
            self.is_superuser = False
        else:
            self.is_staff = True
        super(Site_User, self).save(*args, **kwargs)

    # to check if he is manager or seller it must have branched
    def clean(self):
        if self.user_type > 0:
            print(self.branch)
            if not self.branch:
                raise ValidationError(f"{Site_User.USER_TYPE_CHOICES[self.user_type][1]} Can't Created Without Branch")

    def __str__(self):
        return self.username

    def is_site_admin(self):
        return self.user_type == 0

    def is_branch_manager(self):
        return self.user_type == 1
