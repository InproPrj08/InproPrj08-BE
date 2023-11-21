from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


#학번
class Number(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number


#관심직무
class Interest(models.Model):
    interest = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=False, allow_unicode=True)

    def __str__(self):
        return self.interest

    def save(self, *args, **kwargs):
        self.slug = slugify(self.interest)
        super().save(*args, **kwargs)

#학적상태
class Status(models.Model):
    status = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=False, allow_unicode=True)

    def __str__(self):
        return self.status

    def save(self, *args, **kwargs):
        self.slug = slugify(self.status)
        super().save(*args, **kwargs)


#대학
class College(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=False, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


#전공
class Major(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=False, allow_unicode=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


#user 정보
class CUser(AbstractUser):
    number = models.ForeignKey(Number, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    interest = models.ForeignKey(Interest, on_delete=models.SET_NULL, null=True, blank=True)

#포트폴리오
class Portfolio(models.Model):
    head_image = models.ImageField(upload_to='portfolio/images/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    interest = models.ForeignKey(Interest, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    major = models.BooleanField(default=False, null=True, blank=True)

    author = models.ForeignKey('portfolio.CUser', on_delete=models.CASCADE, related_name='portfolio_entries')
    like_users = models.ManyToManyField(CUser, blank=True, related_name='like_portfolio')

    def __str__(self):
        return f'☆{self.pk}☆{self.title} :: {self.author}'

    def get_absolute_url(self):
            return f'/portfolio/{self.pk}/'

    def update(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        # 다른 필드들도 필요에 따라 업데이트
        self.save()

    def delete(self):
        # 필요에 따라 다른 연관된 객체들도 삭제
        self.delete()

#댓글
class Comment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)