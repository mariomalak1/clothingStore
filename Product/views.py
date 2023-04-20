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
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product with Code {form.data.get('code')} Added Successfully")
        return redirect("admin_panel")
    form = ProductDetailAddForm()
    context = {"form": form}
    return render(request, "Product/add_product_detail.html", context)
