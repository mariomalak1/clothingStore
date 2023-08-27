from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('all_orders_created/<str:cart_code>/', views.all_orders_created, name="all_orders_created"),

    path("create_cart/", views.create_cart, name="create_cart"),

    path('delete_cart/<str:cart_code>/', views.delete_cart, name="delete_cart"),
    path('delete_cart/<str:cart_code>/<str:place>', views.delete_cart, name="delete_cart"),


    path("delete_order/<str:order_id>/<str:order_number>", views.delete_order, name="delete_order"),

    path('get_sizes/', views.get_sizes, name='get_sizes'),
    path("create_order/<str:cart_code>/", views.create_order, name="seller_create_order"),

    path('check_out/<str:cart_code>/', views.check_out, name="check_out"),
    path('check_out_exchange/<str:cart_code>/', views.check_out_exchange, name="check_out_exchange"),


    path('get_cart_code_from_user/', views.get_cart_code_from_user, name="get_cart_code_from_user"),

    path('edit_cart/<str:cart_code>/', views.edit_cart, name="edit_cart"),

    # user urls
    path("user_profile/", views.user_profile, name="user_profile"),
    path("change_password/", views.change_password, name="change_password"),

    path("logout/", LogoutView.as_view(), name= "logout"),
    path("login/", LoginView.as_view(template_name="Seller/login_page.html"), name="login"),
]


