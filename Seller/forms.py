from django import forms
from Invoice.models import Order
from Invoice.models import Buyer
from .models import Seller, Branch

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as django_user
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


class AddSellerForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False)
    email = forms.EmailField(required=False)
    class Meta:
        model = Seller
        fields = ["is_admin", "email", "salary", "phone_number", "national_id", "age", "manager", "branch"]


class AddUserForm(UserCreationForm):
    class Meta:
        model = django_user
        fields = ["username", "password1", "password2"]

class AddNewBranch(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"
