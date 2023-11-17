from django import forms
from portfolio.models import CUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CUser
        fields = ('username', )