from django import forms
from Product.models import ProductDetail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as django_user
from Seller.models import Branch, User

class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

class EditProductCodeForm(forms.Form):
    product_code = forms.CharField(required=True)


class AddUserForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ["username", "password", "email", "salary", "phone_number", "national_id", "age", "branch"]


class AddNewBranch(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"