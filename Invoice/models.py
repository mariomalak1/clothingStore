import random
import string
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from Seller.models import Site_User, Branch
from Product.models import Product as product_model, Size as Product_size
# Create your models here.

class Buyer(models.Model):
    GENDER = (("man", "Man"), ("women", "Women"))
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="Man")

    def __str__(self):
        return self.name

class Cart(models.Model):
    discount = models.PositiveIntegerField(default=0)
    is_percent_discount = models.BooleanField(default=False)
    cart_code = models.CharField(max_length=200, null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    edit_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(Site_User, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    # function to generate code for every cart
    @staticmethod
    def generate_code():
        list_digits_letters = []
        list_digits_letters += string.ascii_lowercase
        list_digits_letters += string.ascii_uppercase
        list_digits_letters += string.digits
        code = ''
        for i in range(9):
            code += random.choice(list_digits_letters)
        return code

    def __str__(self):
        return self.cart_code

    def save(self, *args, **kwargs):
        if not self.pk: # Check if the object is newly created
            code = Cart.generate_code()
            cart_obj = Cart.objects.filter(cart_code = code).first()
            while cart_obj:
                code = Cart.generate_code()
                cart_obj = Cart.objects.get(code = code)
            # generate a new code for the cart
            self.cart_code = code
        super(Cart, self).save(*args, **kwargs)

    def due_by(self):
        return self.created_at + timedelta(days=14)

    def total_price_without_discount(self):
        total = 0
        for order in self.order_set.all():
            if order.product.price_for_branch > 0:
                total += (order.product.price_for_branch * order.quantity)
            else:
                total += (order.product.product_detail.price * order.quantity)
        return total

    def calculate_percent_get_total(self):
        total = self.total_price_without_discount()
        if self.is_percent_discount:
            return ( ( total / 100 ) * self.discount)
        return (self.discount, total)

    def total_price(self):
        discount, total = self.calculate_percent_get_total()
        return (total - discount)

class Order(models.Model):
    product = models.ForeignKey(product_model, on_delete=models.CASCADE)
    size = models.ForeignKey(Product_size, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def clean(self):
        try:
            if self.product:
                pass
        except:
            raise ValidationError("Enter Product")

        if self.quantity <= 0:
            raise ValidationError("You Must Enter Valid Quantity Number")
        if self.quantity > self.product.quantity:
            raise ValidationError("Not Found All This Quantity From This Product In The Branch")

    def total_cost_for_order(self):
        if self.product.price_for_branch > 0:
            return (self.product.price_for_branch * self.quantity)
        else:
            return (self.product.product_detail.price * self.quantity)

    def __str__(self):
        return (self.product.product_detail.name + " - " + str(self.quantity) + " - " + self.cart.cart_code)