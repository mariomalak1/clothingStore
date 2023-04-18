from django import forms
from Invoice.models import Order

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["created_at", "cart"]


class CheckOutForm(forms.Form):
    is_finished = forms.BooleanField(required=True, label="Is Finished")


