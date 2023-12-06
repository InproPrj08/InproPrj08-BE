from django import forms
from django.contrib.auth.forms import UserChangeForm
from portfolio.models import CUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CUser
        fields = ('username', )



class CustomUserChangeForm(UserChangeForm):
    new_username = forms.CharField(max_length=30, required=False)  # Add this line

    class Meta:
        model = CUser
        fields = ('new_username', 'college', 'major', 'number', 'status', 'interests')