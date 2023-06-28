from django.shortcuts import render

# create views here.

def create_invoice(request):
    return render(request, "Invoice/invoice.html")