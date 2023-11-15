from django.shortcuts import render
from .models import Portfolio
from django.views.generic import ListView
# Create your views here.

class PortfolioList(ListView):
    model = Portfolio
    ordering = '-pk'

