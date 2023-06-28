from django import forms
from .models import Product, ProductDetail

class ProductDetailAddForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"

class EditProductCodeForm(forms.Form):
    product_code = forms.CharField(required=True)

class AddProductInBranchForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['branch',]

## this form to edit product in branch, if user is seller he can't edit anything
## if user is manager he can edit quantity only
## if user is admin, he can edit anything
## it must send user_site to this form
## if the user is manager, he can edit product price or quantity, not code
## if he is admin he can edit in anything for the product
class EditProductInBranchForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['branch',]


    def __init__(self, *args, **kwargs):
        user_site = kwargs["user_site"]
        del kwargs["user_site"]
        super().__init__(*args, **kwargs)

        disabled_fields = {}

        if user_site.is_branch_manager():
            for field_name, field in self.fields.items():
                if field_name == "quantity" or field_name == "price_for_branch":
                    pass
                else:
                    field.widget.attrs['disabled'] = True
                    field.required = False
                    disabled_fields['disabled_product_detail'] = forms.CharField(
                        widget=forms.HiddenInput,
                        initial=self.instance.product_detail,
                    )
        elif not user_site.is_site_admin():
            for field_name, field in self.fields.items():
                field.widget.attrs['disabled'] = True

        if disabled_fields:
            self.fields.update(disabled_fields)

    def clean(self):
        cleaned_data = super(EditProductInBranchForm, self).clean()
        disabled_product_detail = cleaned_data.get('disabled_product_detail')
        product_detail = ProductDetail.objects.get(product_code=disabled_product_detail)
        if disabled_product_detail:
            cleaned_data['product_detail'] = product_detail
            del cleaned_data["disabled_product_detail"]
        return cleaned_data
