from django import forms
from .models import Product

class AddProductInBranchForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['branch',]



