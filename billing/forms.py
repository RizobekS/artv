from django import forms

from accounts.models import AuthUsers


class OrderForm(forms.ModelForm):
    class Meta:
        model = AuthUsers
        fields = ['telephone', 'postcode', 'country', 'city', 'street']
