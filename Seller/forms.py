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
        self.fields["product"].queryset = Product_Model.objects.filter(branch=seller_branch, quantity__gt=0)

class CheckOutForm(forms.Form):
    is_finished = forms.BooleanField(required=True, label="Is Finished")


class BuyerForm(forms.ModelForm):
    name = forms.CharField(max_length=145, required=False)
    class Meta:
        model = Buyer
        fields = '__all__'

class GetCartForm(forms.Form):
    cart_code = forms.CharField(max_length=10)


class UserProfile(forms.ModelForm):
    class Meta:
        model = Site_User
        fields = ["username", "user_type", "branch", "salary", "phone_number", "age", "national_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            user_instance = kwargs["instance"]
            if user_instance.user_type > 0:
                for field_name, field in self.fields.items():
                    field.widget.attrs['disabled'] = True
        except:
            pass


class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="New Password Confirmation")

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password1")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2