# forms.py

from django import forms
from .models import YourModel

class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ['content']  # 모델의 필드를 지정