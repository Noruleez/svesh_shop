from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Purchase, Product
from django.core.exceptions import ValidationError


class PurchaseForm(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                validators=[MaxValueValidator(10000), MinValueValidator(1)])
