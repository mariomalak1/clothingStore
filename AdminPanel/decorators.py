from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from Seller.models import User


def is_authenticated_admin_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            if request.user.is_staff:
                return func(request)
            else:
                return HttpResponseForbidden()
    return test_user


def is_authenticated_manager_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            try:
                manager = User.objects.get(id= request.user.id).first()
                if manager.user_type == 1:
                    return func(request)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user


def is_authenticated_admin_or_manager_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            if request.user.is_staff:
                return func(request)
            try:
                manager = User.objects.get(id= request.user.id).first()
                if manager.user_type == 1:
                    return func(request)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
    return test_user

def is_authenticated_seller_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            if request.user.is_staff:
                messages.add_message(request, messages.WARNING, "Choose Branch First To Be In It")
                return redirect("settings")
            try:
                seller = User.objects.get(id = request.user.id).first()
                if seller:
                    if seller.user_type > 0:
                        return func(request)
                    else:
                        messages.add_message(request, messages.WARNING, "Choose Branch First To Be In It")
                        return redirect("settings")
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user