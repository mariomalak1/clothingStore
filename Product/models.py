from django.db import models
from Seller.models import Branch
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=10, null=True, blank=True)
    product_code = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_code