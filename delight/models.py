from django.db import models
from django.contrib.sites.models import Site


class Program(models.Model):
    b_content = models.CharField(max_length=255, null=True, blank=True)
    label_content = models.CharField(max_length=255, null=True, blank=True)
    time_content = models.CharField(max_length=255, null=True, blank=True)
    hit_content = models.IntegerField(null=True, blank=True)
    link_content = models.CharField(max_length=255, null=True, blank=True)
