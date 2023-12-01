from django import forms
from django.contrib.auth.forms import UserChangeForm
from portfolio.models import CUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CUser
        fields = ('username', )



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CUser
        fields = ('username', 'college', 'major', 'number', 'profile_image')