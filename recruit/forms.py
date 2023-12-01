from django import forms
from .models import Comment, Recruit, Interest


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': '댓글을 입력하세요!'}),
    )
    is_anonymous = forms.BooleanField(required=False)
    class Meta:
        model = Comment
        fields = ['text', 'is_anonymous']


class RecruitForm(forms.ModelForm):
    interest_field = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Recruit
        fields = ['title', 'styles','content','interest_field','department','status', 'people', 'deadline', 'file']
