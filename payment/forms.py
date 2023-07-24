from django import forms
from .models import *


class FreeKassaPaymentForm(forms.ModelForm):
    class Meta:
        model = FreeKassaPaymentStatus
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AaioPaymentForm(forms.ModelForm):
    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }
