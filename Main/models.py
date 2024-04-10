from django.db import models

# Create your models here.

class SiteSettings(models.Model):
    SiteName = models.CharField(max_length=250, default="No Name")
    due_by_days = models.PositiveIntegerField(null=True, default=14)
