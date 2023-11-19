from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Number(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number


class College(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Major(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CUser(AbstractUser):
    number = models.ForeignKey(Number, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)

class Portfolio(models.Model):
    head_image = models.ImageField(upload_to='portfolio/images/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey('portfolio.CUser', on_delete=models.CASCADE, related_name='portfolio_entries')
    like_users = models.ManyToManyField(CUser, blank=True, related_name='like_portfolio')
    def __str__(self):
        return f'☆{self.pk}☆{self.title} :: {self.author}'

    def get_absolute_url(self):
            return f'/portfolio/{self.pk}/'

class Comment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)