from django.urls import path
from . import views
urlpatterns = [
    path("create_invoice/<str:cart_code>", views.create_invoice, name="create_invoice"),
    # path("create_invoice_pdf/", views.create_invoice_pdf, name="create_invoice_pdf"),
]

