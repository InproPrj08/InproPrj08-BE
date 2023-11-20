from django.urls import path
from .views import filter_page
from .views import populate_database

app_name ='filter'

urlpatterns = [
    path('', filter_page, name='filter_page'),
    path('api/populate_database/', populate_database, name='populate_database'),
]
