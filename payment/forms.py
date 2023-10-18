from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class FreeKassaPaymentForm(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}),
                                validators=[MaxValueValidator(10000), MinValueValidator(1)])


class AaioPaymentForm(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}),
                                validators=[MaxValueValidator(10000), MinValueValidator(1)])


# class FreeKassaPaymentForm(forms.ModelForm):
#     amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Сумма пополнения'}),
#                                 validators=[MaxValueValidator(10000), MinValueValidator(1)])
#
#     class Meta:
#         model = FreeKassaPaymentStatus
#         fields = ['amount']