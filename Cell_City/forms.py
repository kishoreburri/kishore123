from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Address, Feedback
from django.contrib.auth.forms import User as AuthUser
from django.contrib.auth.models import User

class AddressForm(forms.ModelForm):
    mobile_regex = r'^\+?1?\d{9,15}$'
    mobile_number = forms.RegexField(regex=mobile_regex, max_length=15)

    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code', 'mobile_number']

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


