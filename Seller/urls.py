from django.urls import path
from . import views
urlpatterns = [
    path('all_orders_created/<str:cart_code>/', views.all_orders_created, name="all_orders_created"),

    path("create_cart/", views.create_cart, name="create_cart"),
    path("create_cart/<str:cart_code>/", views.create_cart, name="create_cart"),

    path('delete_cart/<str:cart_code>/', views.delete_cart, name="delete_cart"),


    path("delete_order/<str:order_id>/<str:order_number>", views.delete_order, name="delete_order"),
    path("create_order/<str:cart_code>/", views.create_order, name="seller_create_order"),

    path('check_out/<str:cart_code>/', views.check_out, name="check_out"),


    path('get_cart_code_from_user/', views.get_cart_code_from_user, name="get_cart_code_from_user"),
    path('edit_cart/<str:cart_code>/', views.edit_cart, name="edit_cart"),
    path('check_out_exchange/<str:old_cart_code>/', views.check_out_exchange, name="check_out_exchange"),
]
