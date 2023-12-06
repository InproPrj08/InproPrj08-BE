from django.db import models
from django.urls import reverse

from portfolio.models import CUser, Major, Interest


# Create your models here.
# 합격수기 포트폴리오
class PassPortfolio(models.Model):
    image = models.ImageField(upload_to='pass_portfolio/images/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=30)
    hashtags = models.TextField(max_length=100, blank=True, null=True)
    content = models.TextField()
    styles = models.JSONField(blank=True, null=True)
    interest_field = models.ManyToManyField(Interest, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    company_name = models.CharField(max_length=50)
    company_info = models.TextField()
    anonymous = models.BooleanField(default=False)

    author = models.ForeignKey('portfolio.CUser', on_delete=models.CASCADE, related_name='pass_portfolio_entries')
    like_users = models.ManyToManyField(CUser, blank=True, related_name='pass_like_portfolio')

    def __str__(self):
        return f'☆{self.pk}☆{self.title} :: {self.author}'

    def get_absolute_url(self):
        return reverse('pass_portfolio:pass_portfolio_detail', kwargs={'pk': self.pk})

    def update(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        # 다른 필드들도 필요에 따라 업데이트
        self.save()

    def delete(self, *args, **kwargs):
        # 필요에 따라 다른 연관된 객체들도 삭제
        super().delete(*args, **kwargs)


# 합격 수기 댓글
class PassComment(models.Model):
    pass_portfolio = models.ForeignKey(PassPortfolio, on_delete=models.CASCADE, related_name='pass_portfolio_comments')
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    likes = models.ManyToManyField(CUser, related_name='pass_comment_likes', blank=True)
