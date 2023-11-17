from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('<str:username>/', views.user_detail, name='detail'),
]
