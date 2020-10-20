from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Verify_F

class user_reg(UserCreationForm):
    email_address = forms.CharField(required=True)

    class meta:
        model = User
        fields = ('username','email','password1','password2')

class verification_code(forms.ModelForm):
    class Meta:
        model = Verify_F
        fields = ('verification_code',)      