from django.db import models

# Create your models here.

class recruit(models.Model):
    content = models.TextField()

class YourModel(models.Model):
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk} - {self.content}'