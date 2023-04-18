from django.urls import path
from . import views
urlpatterns = [
    path('check_out/<str:cart_code>/', views.all_in_cart, name= "all_in_cart")
]

