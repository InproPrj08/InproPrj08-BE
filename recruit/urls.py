from django.contrib import admin
from django.urls import path
from . import views
from .views import display_text
from .views import save_text
# from .views import your_view

urlpatterns = [
    path('', views.your_combined_view, name='your_combined_view'),
    path('save_text/', views.save_text, name='save_text'),
    # path('your-url/', your_view, name='your_view'),
    path('display_text/', views.display_text, name='display_text'),
]