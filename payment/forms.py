from django import forms


class PaymentForm(forms.Form):
    amount = forms.IntegerField(max_digits=8, decimal_places=2)
