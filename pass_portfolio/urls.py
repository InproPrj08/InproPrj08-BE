from django.urls import path
from . import views
from .views import PassPortfolioUpdate, PassPortfolioDeleteView, DeleteCommentView

app_name = 'pass_portfolio'

urlpatterns = [
    path('', views.PassPortfolioList.as_view(), name='pass_portfolio_list'),
    path('write/', views.your_combined_view, name='your_combined_view'),
    path('save_text/', views.save_text, name='save_text'),
    path('<int:pk>/', views.PassPortfolioDetail.as_view(), name='pass_portfolio_detail'),
    path('<int:pk>/like/', views.like),
    path('<int:pk>/update/', PassPortfolioUpdate.as_view(), name='pass_portfolio_update'),
    path('<int:pk>/delete/', PassPortfolioDeleteView.as_view(), name='pass_portfolio_delete'),
    path('<int:pk>/delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('<int:pk>/toggle_comment_like/<int:comment_id>/', views.toggle_comment_like, name='toggle_comment_like'),
    path('filterpage/', views.filtersearch_view, name='filtersearch_view'),
]
