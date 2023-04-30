from django.http import JsonResponse
from Invoice.models import Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotFound
from Seller.models import Branch
import calendar
# from Seller.models import Seller as Seller_Model
# function here

# check that user that send the request is admin!!!!
#### make this function can use by manager or admin, admin can view all branches, but manager can see his
def get_data_specific_year_for_statistics(request):
    user_ = get_object_or_404(User, id =request.user.id)
    if user_.is_staff:
        branches = Branch.objects.all()
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
    # elif he is seller and manager
    else:
        return HttpResponseForbidden()


def get_data_by_year_month_for_statistics(request):
    user_ = get_object_or_404(User, id =request.user.id)
    if user_.is_staff:
        branches = Branch.objects.all()
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

    # elif he is seller and manager
    else:
        return HttpResponseForbidden()

def get_data_by_year_month_day_for_statistics(request):
    user_ = get_object_or_404(User, id =request.user.id)
    if user_.is_staff:
        branches = Branch.objects.all()
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
        print(total_in_day_for_branches_list)
        return JsonResponse(total_in_day_for_branches_list, safe=False)

    # elif he is seller and manager
    else:
        return HttpResponseForbidden()

