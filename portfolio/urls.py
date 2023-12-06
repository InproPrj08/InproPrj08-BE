from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import PortfolioUpdate, PortfolioDeleteView, DeleteCommentView

app_name = 'portfolio'

urlpatterns = [
    path('', views.PortfolioList.as_view(), name='portfolio_list'),
    path('write/', views.your_combined_view, name='your_combined_view'),
    path('save_text/', views.save_text, name='save_text'),
    path('<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio_detail'),
    path('<int:pk>/like/', views.like),
    path('<int:pk>/update/', PortfolioUpdate.as_view(), name='portfolio_update'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('search/', views.search_view, name='search_view'),
    path('<int:pk>/delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('<int:pk>/toggle_comment_like/<int:comment_id>/', views.toggle_comment_like, name='toggle_comment_like'),
    path('filterpage/', views.filtersearch_view, name='filtersearch_view'),
]
