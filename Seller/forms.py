from django import forms
from Invoice.models import Order
from Invoice.models import Buyer
from .models import Branch, Site_User
from Product.models import Product as Product_Model
# forms here

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["created_at", "cart"]

    def __init__(self, seller_branch, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.fields["product"].queryset = Product_Model.objects.filter(branch=seller_branch)

class CheckOutForm(forms.Form):
    is_finished = forms.BooleanField(required=True, label="Is Finished")


class BuyerForm(forms.ModelForm):
    name = forms.CharField(max_length=145, required=False)
    class Meta:
        model = Buyer
        fields = '__all__'

class GetCartForm(forms.Form):
    cart_code = forms.CharField(max_length=10)



