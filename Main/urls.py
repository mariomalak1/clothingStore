from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("<str:cart_code>/", views.home_page, name = "home_page"),

    path("admin/admin_panel/", views.admin_panel, name = "admin_panel"),
    path("admin/product_manage/", views.product_manage, name = "product_manage"),
]
