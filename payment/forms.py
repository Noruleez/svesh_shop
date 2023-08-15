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
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}))

    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
        # widgets = {
        #     'amount': forms.TextInput(attrs={'class': 'form-control'}),
        # }

        def clean_amount(self):
            data = self.cleaned_data['amount']
            if data:
                raise ValidationError("TestError", code='test_error')
            else:
                return data
