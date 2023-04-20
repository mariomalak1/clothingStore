from django.urls import path
from . import views
urlpatterns = [
    path("admin/display_all_products_details/", views.display_all_products_details, name="display_all_products_details"),
    path("admin/add_product_detail/", views.add_product_detail, name = "add_product_detail"),
]