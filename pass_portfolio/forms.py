# forms.py
from django import forms
from pass_portfolio.models import PassComment, PassPortfolio
from portfolio.models import Interest


class PassCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '댓글을 입력해주세요!', 'aria-label': 'default input example',
                   'id': 'my-text-input'}),
    )
    is_anonymous = forms.BooleanField(required=False)

    class Meta:
        model = PassComment
        fields = ['text', 'is_anonymous']


class PassPortfolioForm(forms.ModelForm):
    interest_field = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PassPortfolio
        fields = ['title', 'styles', 'hashtags', 'image', 'content', 'interest_field', 'department', 'company_name',
                  'anonymous']
