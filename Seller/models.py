from django.db import models
from django.contrib.auth.models import User as django_user
# Create your models here.

class Seller(django_user):
    salary = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    national_id = models.CharField(max_length=14, null=True, blank=True)
    manager = models.BooleanField(default=False)

class Branch(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250, null=False, blank=True)
    manager = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    phone_branch = models.CharField(max_length=11, null=False, blank=True)