from django.shortcuts import render
from Invoice.models import Cart, Order
# Create your views here.

def create_order(request):
    return render(request, "Seller/create_order.html")