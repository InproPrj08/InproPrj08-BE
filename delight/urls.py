from django.urls import path
from .views import crawl_and_display

app_name = 'delight'

urlpatterns = [
    path('crawl_and_display/', crawl_and_display, name='program_list'),

]
