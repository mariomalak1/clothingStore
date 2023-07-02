from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from Invoice.models import Cart
from Seller.models import Site_User
# from weasyprint import HTML
# create views here.

# def create_invoice_pdf(request):
#     return HttpResponse()


def create_invoice(request, cart_code):
    cart_ = Cart.objects.filter(cart_code=cart_code).first()
    current_user = get_object_or_404(Site_User, id=request.user.id)
    if cart_:
        context = {
            "cart":cart_,
            "current_user":current_user,
        }
        return render(request, "Invoice/invoice.html", context)
    else:
        return Http404()