from django.urls import path
from . import views
urlpatterns = [
    path('all_orders_created/<str:cart_code>/', views.all_orders_created, name="all_orders_created"),
    path('check_out/<str:cart_code>/', views.check_out, name="check_out"),
]

