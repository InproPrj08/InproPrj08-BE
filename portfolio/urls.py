from django.urls import path
from . import views

urlpatterns =[
    path('', views.PortfolioList.as_view()),
]