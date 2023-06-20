from django.db import models
from django.contrib.auth.models import User as Django_User
from Seller.models import Branch
# Create your models here.

class SiteAdmin(Django_User):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
