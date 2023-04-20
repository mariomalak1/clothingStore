from django.db import models
from Product.models import Product as product_model
import random
import string
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
    # buyer_choices = list(Buyer.objects.all().iterator())
    # choices = buyer_choices
    discount = models.PositiveIntegerField(default=0)
    is_percent_discount = models.BooleanField(default=False)
    cart_code = models.CharField(max_length=200, null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    edit_at = models.DateTimeField(null=True, blank=True)

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
        code = Cart.generate_code()
        cart_obj = Cart.objects.filter(cart_code = code).first()
        while cart_obj:
            code = Cart.generate_code()
            cart_obj = Cart.objects.get(code = code)
        # generate a new code for the cart
        self.cart_code = code
        super(Cart, self).save(*args, **kwargs)

    def total_price_without_discount(self):
        total = 0
        for order in self.order_set.all():
            total += (order.product.price * order.quantity)
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
    product = models.ForeignKey(product_model, on_delete= models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def total_for_order(self):
        return (self.product.price * self.quantity)

    def __str__(self):
        return (self.product.name + " - " + str(self.quantity) + " - " + self.cart.cart_code)
