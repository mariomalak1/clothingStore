from django.db import models
from Seller.models import Branch
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("display_all_sizes")


class ProductDetail(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    sizes = models.ManyToManyField(Size, related_name= "products")
    product_code = models.CharField(max_length=150, unique=True, null=False, blank=False)
    price = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.product_code

class Product(models.Model):
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    price_for_branch = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_detail.product_code} + - Q: {self.quantity} + P: {self.price_for_branch if self.price_for_branch != 0 else self.product_detail.price}"

    def clean(self):
        if not self.quantity:
            raise ValidationError("Please Enter Valid Value In Quantity Field")
