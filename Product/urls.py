from django.urls import path
from . import views
urlpatterns = [
    path("add_product_detail/", views.add_product_detail, name = "add_product_detail"),
]