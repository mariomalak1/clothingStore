from django import forms
from .models import ProductDetail, Product

class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

