from django.urls import path
from . import views

urlpatterns = [
    path("add_new_user/", views.add_new_user, name="add_new_user"),
    path("add_new_branch/", views.add_new_branch, name="add_new_branch"),
    path("display_all_branches/", views.display_all_branches, name="display_all_branches"),
    path("edit_product_detail/<str:branch_name>", views.edit_product_detail, name="edit_product_detail"),
    path("delete_branch/<str:branch_name>", views.delete_branch, name="delete_branch"),
    path("edit_branch/<str:branch_name>", views.edit_branch, name="edit_branch"),
    path("display_all_products_details/", views.display_all_products_details, name="display_all_products_details"),
    path("add_product_detail/", views.add_product_detail, name="add_product_detail"),
    path("edit_product_detail/<str:product_code>/", views.edit_product_detail, name="edit_product_detail"),
    path("delete_product_detail/<str:product_code>/", views.delete_product_detail, name="delete_product_detail"),
    path("display_all_carts/", views.display_all_carts, name="display_all_carts"),
]