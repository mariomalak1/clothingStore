from django.urls import path
from . import views
urlpatterns = [
    path('check_out/<str:cart_code>/', views.check_out, name="check_out")
]

