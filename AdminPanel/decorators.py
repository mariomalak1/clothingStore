from django.http import HttpResponseForbidden
from Seller.models import Seller as Seller_model
def is_authenticated_admin_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            if request.user.is_staff:
                func(request)
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
                    func(request)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user


def is_authenticated_seller_decorator(func):
    def test_user(request):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        else:
            try:
                seller = Seller_model.objects.get(id= request.user.id).first()
                if seller:
                    func(request)
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
    return test_user