from django.urls import path
from . import views
urlpatterns = [
    path("display_all_products_in_branch/<int:branch_id>/", views.display_all_products_in_branch, name = "display_all_products_in_branch"),
    path("add_product_in_branch/<int:branch_id>/", views.add_product_in_branch, name = "add_product_in_branch"),
    path("edit_product_in_branch/<int:branch_id>/<int:product_id>/", views.edit_product_in_branch, name = "edit_product_in_branch"),
    path("delete_product_in_branch/<int:branch_id>/<int:product_id>/", views.delete_product_in_branch, name = "delete_product_in_branch"),

    path("display_all_products_details/", views.display_all_products_details, name="display_all_products_details"),
    path("add_product_detail/", views.add_product_detail, name="add_product_detail"),
    path("edit_product_detail/<str:product_code>/", views.edit_product_detail, name="edit_product_detail"),
    path("delete_product_detail/<str:product_code>/", views.delete_product_detail, name="delete_product_detail"),
    path("edit_product_code/<int:product_detail_id>", views.edit_product_code, name="edit_product_code"),

    path("display_all_sizes/", views.sizesListView, name="display_all_sizes"),
    path("add_new_size/", views.addNewSize, name="add_new_size"),
    path("delete_size/<int:size_id>", views.delete_size, name="delete_size"),
    path("edit_size/<int:size_id>", views.updateSize, name="edit_size"),
]