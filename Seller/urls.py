from django.urls import path
from . import views
urlpatterns = [
    path("create_cart/", views.create_cart, name="create_cart"),
    path("delete_order/<str:order_id>/<str:order_number>", views.delete_order, name="delete_order"),
    path("create_order/<str:cart_code>", views.create_order, name="seller_create_order"),
]
