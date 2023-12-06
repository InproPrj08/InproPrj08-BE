from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name='single_page'

urlpatterns = [
    path('', views.landing, name='main_page'),
]

