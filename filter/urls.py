from django.urls import path
from .views import filter_portfolio

urlpatterns = [
    path('filter_portfolio/', filter_portfolio, name='filter_portfolio'),
]
