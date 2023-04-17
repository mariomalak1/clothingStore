from django.contrib import admin
from .models import Cart, Order, Buyer
# Register your models here.

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Buyer)