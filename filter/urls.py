from django.urls import path
from .views import filter_page

app_name ='filter'

urlpatterns = [
    path('', filter_page, name='filter_page'),
]
