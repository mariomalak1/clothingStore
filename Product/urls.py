from django.urls import path
from . import views
urlpatterns = [
    path("add_product_in_branch/<int:branch_id>/", views.add_product_in_branch, name = "add_product_in_branch"),
]