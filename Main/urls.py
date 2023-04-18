from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name = "home_page"),
    path("admin_panel/", views.admin_panel, name = "admin_panel"),
]