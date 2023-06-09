import calendar
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from AdminPanel.decorators import *
from Invoice.models import Cart
from Seller.models import Branch, Site_User
# function here

## make this function can use by manager or admin, admin can view all branches, but manager can see his branch only
@is_authenticated_admin_or_manager_decorator
def get_data_specific_year_for_statistics(request):
    branches = []
    user_ = get_object_or_404(Site_User, id =request.user.id)
    if user_.is_site_admin():
        branches = Branch.objects.all()
    elif user_.is_branch_manager():
        branches = Branch.objects.filter(name=user_.branch.name)
    specific_year = request.GET.get("specific_year")
    total_in_year_for_branch_list = []
    try:
        specific_year = int(specific_year)
        for branch in branches:
            total_in_month_list = []
            for i in range(1, 13):
                carts = Cart.objects.filter(created_at__month=i, created_at__year=specific_year,
                                            created_by__branch=branch).all()
                total_money_in_month = 0
                for cart in carts:
                    # total money for specific month
                    total_money_in_month += cart.total_price()

                total_in_month_list.append({i: total_money_in_month})
            total_in_year_for_branch_list.append({branch.name: total_in_month_list})
    except:
        return HttpResponseNotFound()
    return JsonResponse(total_in_year_for_branch_list, safe=False)

@is_authenticated_admin_or_manager_decorator
def get_data_by_year_month_for_statistics(request):
    branches = []
    user_ = get_object_or_404(Site_User, id =request.user.id)
    if user_.is_site_admin():
        branches = Branch.objects.all()
    elif user_.is_branch_manager():
        branches = Branch.objects.filter(name=user_.branch.name)
    year = request.GET.get("year")
    month = request.GET.get("month")
    total_in_month_for_branch_list = []
    try:
        month = int(month)
        year = int(year)
        range_month = calendar.monthrange(year, month)
        for branch in branches:
            total_in_day_list = []
            for i in range(1,range_month[1] + 1):
                total_money_in_day = 0
                carts = Cart.objects.filter(created_at__month=month, created_at__year=year, created_at__day= i,created_by__branch=branch).all()
                for cart in carts:
                    # total money for specific month
                    total_money_in_day += cart.total_price()

                total_in_day_list.append({i: total_money_in_day})
            total_in_month_for_branch_list.append({branch.name: total_in_day_list})
    except:
        return HttpResponseNotFound()

    return JsonResponse(total_in_month_for_branch_list, safe=False)


@is_authenticated_admin_or_manager_decorator
def get_data_by_year_month_day_for_statistics(request):
    branches = []
    user_ = get_object_or_404(Site_User, id =request.user.id)
    if user_.is_site_admin():
        branches = Branch.objects.all()
    if user_.is_branch_manager():
        branches = Branch.objects.filter(name=user_.branch.name)
    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")
    total_in_day_for_branches_list = []
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        for branch in branches:
            total_money_in_day = 0
            carts = Cart.objects.filter(created_at__month=month, created_at__year=year, created_at__day= day,created_by__branch=branch).all()
            for cart in carts:
                # total money for specific month
                total_money_in_day += cart.total_price()
            total_in_day_for_branches_list.append({branch.name: total_money_in_day})
    except:
        return HttpResponseNotFound()
    return JsonResponse(total_in_day_for_branches_list, safe=False)

@is_authenticated_admin_or_manager_decorator
def get_data_by_year_and_another_for_statistics(request):
    branches = []
    user_ = get_object_or_404(Site_User, id =request.user.id)
    if user_.is_site_admin():
        branches = Branch.objects.all()
    if user_.is_branch_manager():
        branches = Branch.objects.filter(name=user_.branch.name)
    year1 = request.GET.get("year1")
    year2 = request.GET.get("year2")
    total_in_year_for_branches_list = []
    try:
        year1 = int(year1)
        year2 = int(year2)
        diff = 0
        if year1 > year2:
            year1, year2 = year2, year1
        diff = year2 - year1
        for branch in branches:
            total_money_in_years_in_branch = []
            for i in range(diff + 1):
                total_money_in_year_in_branch = 0
                carts = Cart.objects.filter(created_at__year= (year1 + i), created_by__branch=branch).all()
                for cart in carts:
                    total_money_in_year_in_branch += cart.total_price()
                total_money_in_years_in_branch.append({(year1 + i) : total_money_in_year_in_branch})
            total_in_year_for_branches_list.append({branch.name: total_money_in_years_in_branch})
    except:
        return HttpResponseNotFound()
    return JsonResponse(total_in_year_for_branches_list, safe=False)

