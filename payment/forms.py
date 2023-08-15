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
    amount = forms.IntegerField()

    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_amount(self, *args, **kwargs):
            data = self.cleaned_data.get('amount')
            if data == 100:
                raise forms.ValidationError('Не вводи 100')
            else:
                return data
