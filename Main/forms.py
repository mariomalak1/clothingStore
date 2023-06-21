from django import forms
from Seller.models import Branch

class SettingsForm(forms.Form):
    SiteName = forms.CharField(max_length=250, min_length=2, strip=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, label="Admin Current Branch")
