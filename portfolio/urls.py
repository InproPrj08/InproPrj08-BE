from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortfolioList.as_view(), name='portfolio_list'),
    path('<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio_detail'),
    path('<int:pk>/like/', views.like),
    path('search/', views.search_view, name='search_view'),
]
