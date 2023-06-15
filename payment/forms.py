from django import forms
from .models import Balance
from django.core.exceptions import ValidationError


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }