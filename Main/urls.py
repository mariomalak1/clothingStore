from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("<str:cart_code>/", views.home_page, name = "home_page"),

    path("admin/admin_panel/", views.admin_panel, name = "admin_panel"),
    path("admin/manage_product/", views.manage_products, name = "manage_products"),
    path("admin/manage_branches/", views.manage_branches, name = "manage_branches"),
]
