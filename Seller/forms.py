from django import forms
from Invoice.models import Order
from Invoice.models import Buyer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Seller
# forms here

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["created_at", "cart"]


class CheckOutForm(forms.Form):
    is_finished = forms.BooleanField(required=True, label="Is Finished")


class BuyerForm(forms.ModelForm):
    name = forms.CharField(max_length=145, required=False)
    class Meta:
        model = Buyer
        fields = '__all__'

class GetCartForm(forms.Form):
    cart_code = forms.CharField(max_length=10)


class AddUserForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False)
    class Meta:
        model = Seller
        exclude = ["last_login", "is_superuser", "user_permissions", "is_staff", "is_active", "date_joined", "groups"]