from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(null=True)
    link = models.URLField(null=True)
