from django import forms
from .models import Buyer
class BuyerForm(forms.ModelForm):
    name = forms.CharField(max_length=145, required=False)
    class Meta:
        model = Buyer
        fields = '__all__'