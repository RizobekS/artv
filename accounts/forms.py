from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import AuthUsers


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    phone = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = AuthUsers
        fields = ['phone', 'email', 'first_name', 'last_name',  'password1', 'password2', 'birth_date']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = AuthUsers
        fields = ['email', 'first_name', 'last_name',
                  'phone', 'postcode', 'country',
                  'city', 'street', 'birth_date', 'currency']


class UpdateCheckoutProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True)
    phone = forms.CharField(max_length=255, required=True)
    postcode = forms.CharField(max_length=255, required=True)
    country = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    street = forms.CharField(max_length=255, required=True)

    class Meta:
        model = AuthUsers
        fields = ['email', 'phone', 'postcode', 'country',
                  'city', 'street']
