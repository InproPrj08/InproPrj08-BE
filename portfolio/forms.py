# forms.py
from django import forms
from .models import Comment, Portfolio

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'content']
