from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from AdminPanel.decorators import *
from Seller.models import Branch, Site_User
from .forms import AddProductInBranchForm, EditProductInBranchForm, ProductDetailAddForm, EditProductCodeForm, SizeForm
from .models import Product as Product_Model, ProductDetail, Size
# Create your views here.

@is_authenticated_admin_decorator
def sizesListView(request):
    sizes = Size.objects.all()
    context = {
        "object_list": sizes,
    }
    return render(request, "Product/display_all_sizes.html", context)

@is_authenticated_admin_decorator
def addNewSize(request):
    if request.method == "POST":
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("display_all_sizes")
    else:
        form = SizeForm()
    context = {
        "form":form,
        "process_name":"Create",
        "button_name": "Create",
    }
    return render(request, "Product/add_new_size.html", context)

@is_authenticated_admin_decorator
def updateSize(request, size_id):
    size = get_object_or_404(Size, id=size_id)
    if request.method == "POST":
        size_name = size.name
        form = SizeForm(request.POST, instance=size)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, f"Size successfully updated form {size_name} to {form.data.get('name')}")
            form.save()
            return redirect("display_all_sizes")
    else:
        form = SizeForm(instance=size)
    context = {
        "form":form,
        "process_name":"Edit",
        "button_name": "Save",
    }
    return render(request, "Product/add_new_size.html", context)

def delete_size(request, size_id):
    size = get_object_or_404(Size, id=size_id)
    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, f"Size with name {size.name} Successfully Deleted")
        size.delete()
        return redirect("display_all_sizes")
    else:
        context = {
            "size":size,
        }
        return render(request, 'Product/size_delete_confirmation.html', context)



@is_authenticated_admin_decorator
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

@is_authenticated_admin_decorator
def display_all_products_details(request):
    products = ProductDetail.objects.all()
    context = {"products":products}
    return render(request, "Product/display_all_products_details.html", context)

@is_authenticated_admin_decorator
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

@is_authenticated_admin_decorator
def edit_product_detail(request, product_code):
    product_details = get_object_or_404(ProductDetail, product_code=product_code)
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST, instance=product_details)
        form.fields["product_code"].disabled = True
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, f"Product with Code {product_code} Edited Successfully")
            product_details.product_code = form.cleaned_data.get("product_code")
            product_details.name = form.cleaned_data.get("name")
            product_details.sizes.set(form.cleaned_data.get("sizes"))
            product_details.price = form.cleaned_data.get("price")
            product_details.save()
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm(instance=product_details)
        form.fields["product_code"].disabled = True
    context = {"process_name":"Edit", "form":form, "product_details":product_details}
    return render(request, "Product/add_product_detail.html", context)

@is_authenticated_admin_decorator
def edit_product_code(request, product_detail_id):
    product_detail = get_object_or_404(ProductDetail, id = product_detail_id)
    if request.method == "POST":
        form = EditProductCodeForm(request.POST)
        if form.is_valid():
            if form.data.get("product_code") == product_detail.product_code:
                messages.add_message(request, messages.WARNING, "Please Enter The Change You Want To Apply")
                return redirect("edit_product_code",  product_detail_id)
            else:
                another_product_detail = ProductDetail.objects.filter(product_code=form.data.get("product_code")).first()
                if another_product_detail:
                    messages.add_message(request, messages.WARNING, "Sorry, But there's Another Product Code With Same Code You Enter")
                    return redirect("edit_product_code",  product_detail_id)
                else:
                    product_detail.product_code = form.data.get("product_code")
                    messages.add_message(request, messages.SUCCESS, "Product Code Changed Successfully")
                    product_detail.save()
                    return redirect("edit_product_detail", product_detail.product_code)
    else:
        form = EditProductCodeForm()

    form.fields["product_code"].initial = product_detail.product_code
    context = {"form":form, "product_detail":product_detail}

    return render(request, "Product/edit_product_code.html", context)

@is_authenticated_seller_decorator
def add_product_in_branch(request, branch_id):
    branch = get_object_or_404(Branch, id = branch_id)
    seller = get_object_or_404(Site_User, id = request.user.id)
    if seller.branch == branch:
        if request.method == "POST":
            form = AddProductInBranchForm(request.POST)
            if form.is_valid():
                product_ = form.instance
                product_.branch = branch
                if product_.product_detail.price == 0 and product_.price_for_branch == 0:
                    messages.add_message(request, messages.WARNING, "Note That The Price For The Product you Choose Is 0 And You Enter 0 For It's Price In Your Branch !!!")
                elif product_.price_for_branch == 0:
                    product_.price_for_branch = product_.product_detail.price

                # show if found in the branch the same product, to add to it the new quantity he wants to add
                another_product_with_same_data = Product_Model.objects.filter(product_detail = product_.product_detail, price_for_branch = product_.price_for_branch, branch = product_.branch).first()
                if another_product_with_same_data:
                    another_product_with_same_data.quantity += product_.quantity
                    another_product_with_same_data.save()
                    messages.add_message(request, messages.SUCCESS, f"Product Of Code {product_.product_detail.product_code} Add Successfully To The Old Stuff")
                else:
                    form.save()
                    messages.add_message(request, messages.SUCCESS, f"Product Of Code {product_.product_detail.product_code} Add Successfully")
                return redirect("add_product_in_branch", branch.id)
        else:
            form = AddProductInBranchForm()
        context = {
            "form":form,
            "branch": branch,
            "process_name":"Add New",
            "button_name":"Add",
        }
        return render(request, "Product/add_product_in_branch.html", context)
    else:
        messages.add_message(request, messages.WARNING, "This Not Your Branch To Add Product In!!")
        return redirect("home_page")

@is_authenticated_seller_decorator
def display_all_products_in_branch(request, branch_id):
    branch = get_object_or_404(Branch, id = branch_id)
    products = Product_Model.objects.filter(branch=branch).all()
    # Product_Model.product_detail.sizes.count()
    context = {
        "products":products,
        "branch":branch,
    }
    return render(request, "Product/display_all_products_in_branch.html", context)

@is_authenticated_admin_or_manager_decorator
def edit_product_in_branch(request, branch_id, product_id):
    branch = get_object_or_404(Branch, id = branch_id)
    product = get_object_or_404(Product_Model, id = product_id)
    user_site = get_object_or_404(Site_User, id = request.user.id)

    if request.method == "POST":
        form = EditProductInBranchForm(request.POST, instance=product, user_site=user_site)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Product Save Successfully")
            return redirect("home_page")
    else:
        form = EditProductInBranchForm(instance=product, user_site= user_site)
    context = {
        "form": form,
        "branch": branch,
        "process_name": "Edit",
        "button_name": "Save",
    }
    return render(request, "Product/add_product_in_branch.html", context)

@is_authenticated_admin_decorator
def delete_product_in_branch(request, branch_id, product_id):
    branch = get_object_or_404(Branch, id=branch_id)
    product = get_object_or_404(Product_Model, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.add_message(request, messages.SUCCESS, f"All Products With Code {product.product_detail} Delete From Branch {branch.name} Successfully Deleted")
        return redirect("display_all_products_in_branch", branch.id)
    else:
        product
        context = {"branch":branch, "product":product}
        return render(request, "Product/delete_product_in_branch.html", context)