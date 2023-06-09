from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Address, Feedback
from django.contrib.auth.forms import User as AuthUser


class AddressForm(forms.ModelForm):
    mobile_regex = r'^\+?1?\d{9,15}$'
    mobile_number = forms.RegexField(regex=mobile_regex, max_length=15)

    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'country', 'zip_code', 'mobile_number']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'password1', 'password2')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
