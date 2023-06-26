from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as django_user
from django.contrib.auth.hashers import make_password

from Product.models import ProductDetail
from Seller.models import Branch, Site_User

# Forms Here
class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

class EditProductCodeForm(forms.Form):
    product_code = forms.CharField(required=True)


class AddSellerForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password Confirmation")
    user_type = forms.ChoiceField(choices=Site_User.USER_TYPE_CHOICES, label="User Permision")
    class Meta:
        model = Site_User
        fields = ["username", "password1", "password2", "user_type","email", "branch", "salary", "phone_number", "national_id", "age"]

    def clean_branch(self):
        branch = self.cleaned_data.get("branch")
        if int(self.cleaned_data.get("user_type")) == 0:
            return branch
        else:
            if branch is None:
                raise forms.ValidationError(f"User Must Have Branch Or Make Him Admin")
            return branch

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.password = make_password(password)  # Hash the password
        if commit:
            user.save()
        return user


class AddAdmin(AddSellerForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    user_type = forms.ChoiceField(choices=Site_User.USER_TYPE_CHOICES)



class AddNewBranch(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"

class EditBranchForm(forms.ModelForm):
    branch = forms.CharField(max_length=250, min_length=2, strip=True)
    class Meta:
        model = Branch
        fields = ["branch", "phone_branch", "address"]

class EditUserForm(forms.ModelForm):
    class Meta:
        model = Site_User
        fields = ["username", "user_type", "branch", "salary", "phone_number", "age", "national_id"]