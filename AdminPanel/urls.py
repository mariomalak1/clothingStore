from django.urls import path
from . import views
from . import ajax_request_statistics
urlpatterns = [
    path("add_new_user/", views.add_new_user, name="add_new_user"),
    path("display_all_users/", views.display_all_users, name="display_all_users"),
    path("get_user/<int:user_id>", views.get_user, name="get_user"),

    path("add_new_branch/", views.add_new_branch, name="add_new_branch"),
    path("display_all_branches/", views.display_all_branches, name="display_all_branches"),
    path("delete_branch/<str:branch_name>", views.delete_branch, name="delete_branch"),
    path("edit_branch/<str:branch_name>", views.edit_branch, name="edit_branch"),


    path("display_all_products_details/", views.display_all_products_details, name="display_all_products_details"),
    path("add_product_detail/", views.add_product_detail, name="add_product_detail"),
    path("edit_product_detail/<str:product_code>/", views.edit_product_detail, name="edit_product_detail"),
    path("delete_product_detail/<str:product_code>/", views.delete_product_detail, name="delete_product_detail"),


    path("display_all_carts/", views.display_all_carts, name="display_all_carts"),

    path("display_all_sizes/", views.SizesListView.as_view(), name="display_all_sizes"),
    path("add_new_size/", views.SizeCreateView.as_view(), name="add_new_size"),
    path("delete_size/<int:pk>", views.SizeDeleteView.as_view(), name="delete_size"),
    path("edit_size/<int:pk>", views.SizeUpdateView.as_view(), name="edit_size"),


    path("edit_product_code/<int:product_detail_id>", views.edit_product_code, name="edit_product_code"),
    path("show_statistics/", views.show_statistics, name="show_statistics"),

    path("ajax_request/get_data_specific_year_for_statistics/", ajax_request_statistics.get_data_specific_year_for_statistics, name="get_data_specific_year_for_statistics"),
    path("ajax_request/get_data_by_year_month_for_statistics/", ajax_request_statistics.get_data_by_year_month_for_statistics, name="get_data_by_year_month_for_statistics"),
    path("ajax_request/get_data_by_year_month_day_for_statistics/", ajax_request_statistics.get_data_by_year_month_day_for_statistics, name="get_data_by_year_month_day_for_statistics"),
    path("ajax_request/get_data_by_year_and_another_for_statistics/", ajax_request_statistics.get_data_by_year_and_another_for_statistics, name="get_data_by_year_and_another_for_statistics"),
]

# path("edit_product_detail/<str:branch_name>", views.edit_product_detail, name="edit_product_detail"),