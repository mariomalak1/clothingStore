from django import forms
from Invoice.models import Order
from Invoice.models import Buyer
from .models import Seller, Branch
from Product.models import Product as Product_Model
# forms here

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["created_at", "cart"]

        def get_all_sizes_of_product_in_list():
            lis = []
            for product in Product_Model.objects.all():
                lis.append(product.product_detail.sizes.count())
            return lis

        widgets = {
            "size": forms.Select(attrs={'onChange': 'change_sizes()'}),
            "product": forms.Select(attrs={"sizes":get_all_sizes_of_product_in_list()}),
        }


    class Media:
        js = ('JS/custom_main.js',)

class CheckOutForm(forms.Form):
    is_finished = forms.BooleanField(required=True, label="Is Finished")


class BuyerForm(forms.ModelForm):
    name = forms.CharField(max_length=145, required=False)
    class Meta:
        model = Buyer
        fields = '__all__'

class GetCartForm(forms.Form):
    cart_code = forms.CharField(max_length=10)



