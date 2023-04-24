from django.shortcuts import render, redirect, get_object_or_404
from Product.models import ProductDetail, Product
from .forms import ProductDetailAddForm, AddUserForm, AddSellerForm, AddNewBranch
from django.contrib import messages
from Seller.models import Branch
from Invoice.models import Cart, Order
from .filters import CartFilter
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from Product.models import Size
# Create your views here.

class SizesListView(ListView):
    model = Size
    template_name = "AdminPanel/display_all_sizes.html"

class SizeCreateView(CreateView):
    model = Size
    fields = "__all__"
    template_name = "AdminPanel/add_new_size.html"
    extra_context = {"process_name": "Create", "button_name":"Create"}

class SizeUpdateView(UpdateView):
    model = Size
    fields = "__all__"
    template_name = "AdminPanel/add_new_size.html"
    extra_context = {"process_name": "Edit", "button_name":"Save"}

class SizeDeleteView(DeleteView):
    model = Size
    template_name = "AdminPanel/size_delete_confirmation.html"
    context_object_name = "size"
    success_url = "/store/admin_panel/display_all_sizes"

def add_product_detail(request):
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product with Code {form.data.get('code')} Added Successfully")
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm()
    return render(request, "AdminPanel/add_product_detail.html", {"form": form, "process_name":"Add"})

def display_all_products_details(request):
    products = ProductDetail.objects.all()
    context = {"products":products}
    return render(request, "AdminPanel/display_all_products_details.html", context)

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
        return render(request, "AdminPanel/product_detail_delete_confirmation.html", context)

def edit_product_detail(request, product_code):
    product_details = get_object_or_404(ProductDetail, product_code=product_code)
    if request.method == "POST":
        form = ProductDetailAddForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, f"Product with Code {product_code} Edited Successfully")
            product_details.product_code = form.cleaned_data.get("product_code")
            product_details.name = form.cleaned_data.get("name")
            product_details.size = form.cleaned_data.get("size")
            product_details.price = form.cleaned_data.get("price")
            product_details.save()
            return redirect("display_all_products_details")
    else:
        form = ProductDetailAddForm(instance=product_details)
    context = {"process_name":"Edit", "form":form}
    return render(request, "AdminPanel/add_product_detail.html", context)

def display_all_carts(request):
    carts = Cart.objects.all()
    carts.filter()
    total_money_entered = 0
    cart_filter = CartFilter(data= request.GET, queryset=carts)
    for cart in carts:
        total_money_entered += cart.total_price()
    context = {
        "carts":cart_filter.qs,
        "total_money_entered": total_money_entered,
        "cart_filter":cart_filter,
    }
    return render(request, "AdminPanel/display_all_carts.html", context)

def add_new_user(request):
    if request.method == "POST":
        form_user = AddUserForm(request.POST)
        form_seller = AddSellerForm(request.POST)
        if form_seller.is_valid() and form_user.is_valid():
            form_user.save()
            form_seller.instance.user = form_user.instance
            if form_seller.data.get("is_admin"):
                form_user.instance.is_staff = True
            form_user.save()
            form_seller.save()
            username = form_user.cleaned_data.get("username")
            messages.success(request, f"Seller with Username {username} have been created")
            return redirect("admin_panel")
    else:
        form_user = AddUserForm()
        form_seller = AddSellerForm()

    context = {"form_user":form_user, "form_seller":form_seller}
    return render(request, "AdminPanel/register.html", context)

def add_new_branch(request):
    if request.method == "POST":
        form = AddNewBranch(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Congratulations, Branch Successfully Opened In System, You Can Add To It Sellers and Managers from Admin Panel")
            return redirect("display_all_branches")
    else:
        form = AddNewBranch()
    return render(request, "AdminPanel/add_new_branch.html", {"form":form, "process_name": "Open", "button_name": "Create"})

def display_all_branches(request):
    branches = Branch.objects.all()
    context = {"branches":branches}
    return render(request, "AdminPanel/display_all_branches.html", context)

def edit_branch(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        form = AddNewBranch(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, f"Branch With Name {branch_name} Edited Successfully")
            branch.name = form.cleaned_data.get("name")
            branch.address = form.cleaned_data.get("address")
            branch.phone_branch = form.cleaned_data.get("phone_branch")
            branch.save()
            return redirect("display_all_branches")
    else:
        form = AddNewBranch(instance=branch)
    context = {"process_name":"Edit", "form":form, "button_name":"Save"}
    return render(request, "AdminPanel/add_new_branch.html", context)

def delete_branch(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        branch.delete()
        messages.add_message(request, messages.SUCCESS, f"Branch With Name {branch_name} Successfully Deleted")
        return redirect("display_all_branches")
    else:
        total_number_of_employees = branch.seller_set.count()
        total_number_of_products = 0
        for product_branch in branch.product_set.all():
            total_number_of_products += product_branch.quantity

        context = {"branch":branch, "total_number_of_employees":total_number_of_employees, "total_number_of_products":total_number_of_products}
        return render(request, "AdminPanel/branch_delete_confirmation.html", context)