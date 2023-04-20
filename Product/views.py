from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductDetail, Product
from .forms import ProductDetailAddForm
from django.contrib import messages

# Create your views here.

# it will be by admin only, and this to be for all branches
def add_product_detail(request):
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST)
        if form.is_valid():
            print("mario")
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product with Code {form.data.get('code')} Added Successfully")
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm()
    return render(request, "Product/add_product_detail.html", {"form": form})

def display_all_products_details(request):
    products = ProductDetail.objects.all()
    context = {"products":products}
    return render(request, "Product/display_all_products_details.html", context)

# def delete_product_detail(request, product_):
#
#     return render(request, "Seller/delete_confirmation.html", context)

