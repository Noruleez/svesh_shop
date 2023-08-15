from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import *


class FreeKassaPaymentForm(forms.ModelForm):
    class Meta:
        model = FreeKassaPaymentStatus
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AaioPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(required=False, error_messages={'invalid': 'Enter a valid phone number'})
    # widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'})
    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
        # widgets = {
        #     'amount': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise ValidationError("Введите положительное число")
        if int(data) != float(data):
            raise ValidationError("Введите целое число")
        return data