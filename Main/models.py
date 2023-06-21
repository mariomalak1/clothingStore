from django.db import models

# Create your models here.

class SiteSettings(models.Model):
    SiteName = models.CharField(max_length=250)
