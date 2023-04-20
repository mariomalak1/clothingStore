from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductDetail, Product
from .forms import ProductDetailAddForm
from django.contrib import messages
from Seller.models import Branch
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

# it will be by admin only, and this to be for all branches
def add_product_detail(request):
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product with Code {form.data.get('code')} Added Successfully")
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm()
    return render(request, "Product/add_product_detail.html", {"form": form, "process_name":"Add"})

def display_all_products_details(request):
    products = ProductDetail.objects.all()
    context = {"products":products}
    return render(request, "Product/display_all_products_details.html", context)

def delete_product_detail(request, product_code):
    product_details = get_object_or_404(ProductDetail, product_code=product_code)
    if request.method == "POST":
        product_details.delete()
        messages.add_message(request, messages.SUCCESS, f"Product with Code {product_code} Successfully Deleted")
        return redirect("display_all_products_details")
    else:
        branches = Branch.objects.all()
        total_number_of_products_in_branches = 0
        for branch in branches:
            for product_ in branch.product_set.filter(product_detail=product_details).all():
                total_number_of_products_in_branches += product_.quantity

        context = {"product":product_details, "total_number_of_products_in_branches":total_number_of_products_in_branches}
        return render(request, "Product/product_detail_delete_confirmation.html", context)

def edit_product_detail(request, product_code):
    product_details = get_object_or_404(ProductDetail, product_code=product_code)
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST)
        if form.is_valid():
            product_details.product_code = form.cleaned_data.get("product_code")
            product_details.name = form.cleaned_data.get("name")
            product_details.size = form.cleaned_data.get("size")
            product_details.price = form.cleaned_data.get("price")
            product_details.save()
            messages.add_message(request, messages.SUCCESS, f"Product with Code {form.data.get('code')} Edited Successfully")
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm(instance=product_details)
    context = {"process_name":"Edit", "form":form}
    return render(request, "Product/add_product_detail.html", context)