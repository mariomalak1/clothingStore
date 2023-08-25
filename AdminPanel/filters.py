import django_filters
from django.db.models import Count
from Seller.models import Branch
from Invoice.models import Cart, Order
from django import forms

class CartFilter(django_filters.FilterSet):

    def all_branches():
        branches = Branch.objects.all()
        lis = []
        for branch in branches:
            tup = (branch, branch)
            lis.append(tup)
        return tuple(lis)

    branch_name = django_filters.ChoiceFilter(choices = all_branches, field_name= "branch", label="Branch Name", method="data_by_branch_name")
    from_date = django_filters.DateFilter(field_name= "created_at", label="From Date", lookup_expr= "gt", widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = django_filters.DateFilter(field_name= "created_at", label="To Date", lookup_expr= "lt", widget=forms.DateInput(attrs={'type': 'date'}))
    edited = django_filters.BooleanFilter(field_name='edit_at', label="Edited ? ", method="data_by_edited__or_not")
    cart_code = django_filters.CharFilter(field_name="cart_code", method="data_by_cart_code_like")
    number_of_orders = django_filters.NumberFilter(label="Number Of Orders Greater than", field_name="order_set", method="data_by_number_of_orders")
    ## number of orders

    def data_by_number_of_orders(self, queryset, name, value):
        return queryset.annotate(count=Count('order')).filter(count=value)

    def data_by_edited__or_not(self, queryset, name, value):
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: not value})

    def data_by_cart_code_like(self, queryset, name, value):
        return queryset.filter(cart_code__icontains=value)

    def data_by_branch_name(self, queryset, name, value):
        return queryset.filter(branch__name=value)


    class Meta:
        model = Cart
        fields = ["cart_code", "discount", "created_by", "from_date", "to_date", "edited_by", "edit_at", "is_finished"]

class CartFilterForManager(CartFilter):
    branch_name = None