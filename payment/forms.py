from django import forms
from django.core.exceptions import ValidationError

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

        def clean_amount(self, *args, **kwargs):
            data = self.cleaned_data.get('amount')
            if data == 100:
                raise ValidationError('Не вводи 100')
            else:
                return data
