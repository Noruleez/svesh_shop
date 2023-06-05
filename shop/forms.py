from django import forms
from .models import Purchase, Product
from django.core.exceptions import ValidationError


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Purchase.objects.filter(slug=new_slug).count():
            raise ValidationError(f'Slug must be unique. We have "{new_slug}" slug already')

        return new_slug