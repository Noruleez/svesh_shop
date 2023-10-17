from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import FreeKassaPaymentStatus, AaioPaymentStatus


class FreeKassaPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}), validators=[MaxValueValidator(10000),
                                                                                                               MinValueValidator(1)])
    class Meta:
        model = FreeKassaPaymentStatus
        fields = ['amount']


class AaioPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}), validators=[MaxValueValidator(10000),
                                                                                                               MinValueValidator(1)])
    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
