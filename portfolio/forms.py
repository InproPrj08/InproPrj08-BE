# forms.py
from django import forms
from .models import Comment, Portfolio

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': '댓글을 입력하세요!'}),
    )
    is_anonymous = forms.BooleanField(required=False)
    class Meta:
        model = Comment
        fields = ['text', 'is_anonymous']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'content']
