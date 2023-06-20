from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from Seller.models import Seller as Seller_model


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
                seller = Seller_model.objects.get(id= request.user.id).first()
                if seller.manager:
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
                seller = Seller_model.objects.filter(user_obj=request.user.id).first()
                if seller.manager:
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
                seller = Seller_model.objects.filter(user_obj = request.user.id).first()
                if seller:
                    return func(request)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user