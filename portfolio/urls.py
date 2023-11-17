from django.urls import path
from . import views

urlpatterns =[
    path('', views.PortfolioList.as_view()),
    path('<int:pk>/', views.PortfolioDetail.as_view(), name='portfoliodetail'),
    path('<int:pk>/like/', views.like),
    path('search/', views.search_view, name='search_view'),
]