from django.urls import path
from . import views
urlpatterns = [
    path("admin/display_all_products_details/", views.display_all_products_details, name="display_all_products_details"),
    path("admin/add_product_detail/", views.add_product_detail, name = "add_product_detail"),
    path("admin/edit_product_detail/<str:product_code>/", views.edit_product_detail, name = "edit_product_detail"),
    path("admin/delete_product_detail/<str:product_code>/", views.delete_product_detail, name = "delete_product_detail"),
]