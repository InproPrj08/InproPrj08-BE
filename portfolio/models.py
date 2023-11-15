from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Portfolio(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'☆{self.pk}☆{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/portfolio/{self.pk}/'
