from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import *


class FreeKassaPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}), validators=[MaxValueValidator(10000),
                                                                                                               MinValueValidator(1)])
    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']


class AaioPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}), validators=[MaxValueValidator(10000),
                                                                                                               MinValueValidator(1)])
    class Meta:
        model = AaioPaymentStatus
        fields = ['amount']
        # widgets = {
        #     'amount': forms.TextInput(attrs={'class': 'form-control'}),
        # }
    #
    # def clean_amount(self):
    #     data = self.cleaned_data['amount']
    #     if data <= 0:
    #         raise ValidationError("Введите положительное число")
    #     if int(data) != float(data):
    #         raise ValidationError("Введите целое число")
    #     return data