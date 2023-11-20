from django.db import models

# Create your models here.

class Student(models.Model):
    STATUS_CHOICES = [
        ('재학생', '재학생'),
        ('휴학생', '휴학생'),
        ('취준생', '취준생'),
    ]

    INTEREST_CHOICES = [
        ('경영', '경영'),
        ('교육', '교육'),
        ('인터넷', '인터넷'),
        ('연구', '연구'),
        ('마케팅', '마케팅'),
        ('미디어', '미디어'),
        ('의료', '의료'),
        ('디자인', '디자인'),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)

    def __str__(self):
            return self.name


class Department(models.Model):
     name = models.CharField(max_length=100)

     def __str__(self):
         return self.name


class SubDepartment(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department.name} - {self.name}"




