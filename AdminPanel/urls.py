from django.urls import path
from . import views
from . import ajax_request_statistics
urlpatterns = [
    path("add_new_user/", views.add_new_user, name="add_new_user"),
    path("display_all_users/", views.display_all_users, name="display_all_users"),
    path("get_user/<int:user_id>", views.get_user, name="get_user"),
    path("delete_user/<int:user_id>", views.delete_user, name="delete_user"),

    path("add_new_branch/", views.add_new_branch, name="add_new_branch"),
    path("display_all_branches/", views.display_all_branches, name="display_all_branches"),
    path("delete_branch/<str:branch_name>", views.delete_branch, name="delete_branch"),
    path("edit_branch/<str:branch_name>", views.edit_branch, name="edit_branch"),

    path("display_all_carts/", views.display_all_carts, name="display_all_carts"),

    path("show_statistics/", views.show_statistics, name="show_statistics"),

    path("ajax_request/get_data_specific_year_for_statistics/", ajax_request_statistics.get_data_specific_year_for_statistics, name="get_data_specific_year_for_statistics"),
    path("ajax_request/get_data_by_year_month_for_statistics/", ajax_request_statistics.get_data_by_year_month_for_statistics, name="get_data_by_year_month_for_statistics"),
    path("ajax_request/get_data_by_year_month_day_for_statistics/", ajax_request_statistics.get_data_by_year_month_day_for_statistics, name="get_data_by_year_month_day_for_statistics"),
    path("ajax_request/get_data_by_year_and_another_for_statistics/", ajax_request_statistics.get_data_by_year_and_another_for_statistics, name="get_data_by_year_and_another_for_statistics"),
]

# path("edit_product_detail/<str:branch_name>", views.edit_product_detail, name="edit_product_detail"),