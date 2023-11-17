from django.db import models

# Create your models here.

class Student(models.Model):
    STATUS_CHOICES = [
        ('재학생', '재학생'),
        ('휴학생', '휴학생'),
        ('졸업생', '졸업생'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.status}"

