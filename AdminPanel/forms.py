from django import forms
from Product.models import ProductDetail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as django_user
from Seller.models import Seller, Branch

class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

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