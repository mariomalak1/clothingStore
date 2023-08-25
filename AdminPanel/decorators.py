from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from Seller.models import Site_User


def is_authenticated_admin_decorator(func):
    def test_user(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            # try:
                admin_ = Site_User.objects.get(id=request.user.id)
                if admin_.user_type == 0:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            # except:
            #     return HttpResponseForbidden()

    return test_user

def is_authenticated_manager_decorator(func):
    def test_user(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            try:
                manager = Site_User.objects.get(id=request.user.id)
                if manager.user_type == 1:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()

    return test_user

def is_authenticated_admin_or_manager_decorator(func):
    def test_user(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            try:
                user_ = Site_User.objects.get(id=request.user.id)
                if (user_.is_site_admin()) or (user_.is_branch_manager()):
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()

    return test_user

# seller and manager decorator
def is_authenticated_seller_decorator(func):
    def test_user(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect("login")
        else:
            try:
                seller = Site_User.objects.get(id=request.user.id)
                if seller:
                    if seller.is_can_be_seller():
                        return func(request, *args, **kwargs)
                    else:
                        if seller.is_site_admin():
                            messages.add_message(request, messages.WARNING, "Choose Branch First To Be In It")
                            return redirect("settings")
                        else:
                            return HttpResponseForbidden()
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user