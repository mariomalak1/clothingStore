from django.db import models
from Seller.models import Branch
# Create your models here.

class ProductDetail(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    product_code = models.CharField(max_length=150, unique=True)
    price = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.product_code


class Product(models.Model):
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    price_for_branch = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_detail.product_code + " - " + str(self.quantity)
