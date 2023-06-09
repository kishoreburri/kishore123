from django import forms
from .models import Address
from .models import Feedback
from django.contrib.auth.forms import UserCreationForm, User


class AddressForm(forms.ModelForm):
    mobile_regex = r'^\+?1?\d{9,15}$' 
    mobile_number = forms.RegexField(regex=mobile_regex, max_length=15)

    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'country', 'zip_code', 'mobile_number']



class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['date_of_birth', 'mobile_number']



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message',]