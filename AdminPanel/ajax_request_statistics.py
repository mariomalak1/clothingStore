from django.http import JsonResponse
from Invoice.models import Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from Seller.models import Branch
# from Seller.models import Seller as Seller_Model
# function here

# check that user that send the request is admin!!!!
#### make this function can use by manager or admin, admin can view all branches, but manager can see his
def get_data_specific_year_for_statistics(request):
    user_ = get_object_or_404(User, id =request.user.id)
    branches = Branch.objects.all()
    if user_.is_staff:
        specific_year = request.GET.get("specific_year")
        total_in_year_for_branch_list = []
        for branch in branches:
            total_in_month_list = []
            for i in range(1,13):
                carts = Cart.objects.filter(created_at__month=i, created_at__year=specific_year, created_by__branch= branch).all()
                total_money_in_month = 0
                for cart in carts:
                    # total money for specific month
                    total_money_in_month += cart.total_price()

                total_in_month_list.append({i:total_money_in_month})
            total_in_year_for_branch_list.append({branch.name:total_in_month_list})

        return JsonResponse(total_in_year_for_branch_list, safe=False)
    # elif he is seller and manager
    else:
        return HttpResponseForbidden()