from django.urls import path
from .views import crawl_and_display
from .views import index

app_name = 'delight'

urlpatterns = [
    path('crawl_and_display/', crawl_and_display, name='program_list'),
    path('index/', index, name='index')
    # 다른 URL 패턴이 있다면 계속해서 추가할 수 있습니다.
]