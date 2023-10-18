from django import forms
from .models import Purchase, Product
from django.core.exceptions import ValidationError


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }
