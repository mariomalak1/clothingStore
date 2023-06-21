from django import forms
from Product.models import ProductDetail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as django_user
from Seller.models import Branch, Site_User

class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

class EditProductCodeForm(forms.Form):
    product_code = forms.CharField(required=True)


class AddUserForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = django_user
        fields = ["username", "password", "email"]

class AddSellerForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)
    class Meta:
        model = Site_User
        fields = ["salary", "phone_number", "national_id", "age", "branch"]

class AddAdmin(AddSellerForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)


class AddNewBranch(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"