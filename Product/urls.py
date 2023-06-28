from django.urls import path
from . import views
urlpatterns = [
    path("display_all_products_in_branch/<int:branch_id>/", views.display_all_products_in_branch, name = "display_all_products_in_branch"),
    path("add_product_in_branch/<int:branch_id>/", views.add_product_in_branch, name = "add_product_in_branch"),
    path("edit_product_in_branch/<int:branch_id>/<int:product_id>/", views.edit_product_in_branch, name = "edit_product_in_branch"),
    path("delete_product_in_branch/<int:branch_id>/<int:product_id>/", views.delete_product_in_branch, name = "delete_product_in_branch"),
]