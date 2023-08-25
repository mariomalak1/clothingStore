from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from Invoice.models import Cart
from Seller.models import Site_User, Branch
from .forms import SettingsForm
from .models import SiteSettings
from AdminPanel.decorators import *
# Create your views here.

@is_authenticated_seller_decorator
def home_page(request, cart_code=None):
    user = get_object_or_404(Site_User, id=request.user.id)
    context = {"seller": user}
    if cart_code:
        cart = Cart.objects.filter(cart_code=cart_code).first()
        if cart:
            context["cart_code"] = cart_code
            return render(request, "Main/home_page.html", context)
        else:
            messages.add_message(request, messages.WARNING, "No Card Found with This Code")
            return render(request, "Main/home_page.html", context)
    else:
        return render(request, "Main/home_page.html", context)

@is_authenticated_admin_or_manager_decorator
def admin_panel(request):
    user_ = get_object_or_404(Site_User, id = request.user.id)
    if user_.is_site_admin():
        page_title = "Admin Panel"
    elif user_.is_branch_manager():
        page_title = "Manager Panel"
    else:
        return HttpResponseForbidden()
    context = {
        "page_title": page_title,
        "user":request.user,
    }
    return render(request, "Main/admin_panel.html", context)

@is_authenticated_admin_decorator
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            settingsSaveChanges(request, form)
            messages.add_message(request, messages.SUCCESS, "Settings Saved Successfully")
            return redirect("settings")
    else:
        form = SettingsForm()
        settingsFillFields(request, form)
    context = {
        "form":form,
    }
    return render(request, "Main/settings.html", context)

def settingsFillFields(request, form):
    user_ = Site_User.objects.get(id = request.user.id)
    site_name = SiteSettings.objects.all().first()
    form["SiteName"].initial = site_name.SiteName
    if user_:
        if user_.branch:
            form["branch"].initial = user_.branch

def settingsSaveChanges(request, settingsForm):
    settings_model = SiteSettings.objects.all().first()
    settings_model.SiteName = settingsForm.cleaned_data.get('SiteName')
    settings_model.due_by_days = settingsForm.cleaned_data.get("due_by_days")
    settings_model.save()

    user_ = Site_User.objects.get(id = request.user.id)
    branch = settingsForm.cleaned_data.get("branch")
    user_.branch = branch
    user_.save()
