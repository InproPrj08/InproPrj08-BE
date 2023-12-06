from django.urls import path
from . import views
from .views import DeleteCommentView

app_name = 'recruit'

urlpatterns = [
    path('', views.RecruitList.as_view(), name='recruit_list'),
    path('write/', views.your_combined_view, name='your_combined_view'),
    path('save_text/', views.save_text, name='save_text'),
    path('<int:pk>/', views.RecruitDetail.as_view(), name='recruit_detail'),
    path('<int:pk>/like/', views.like),
    path('<int:pk>/update/', views.RecruitUpdate.as_view(), name='recruit_update'),
    path('<int:pk>/delete/', views.RecruitDeleteView.as_view(), name='recruit_delete'),
    path('<int:pk>/delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('<int:pk>/toggle_comment_like/<int:comment_id>/', views.toggle_comment_like, name='toggle_comment_like'),
    path('filterpage/', views.filtersearch_view, name='filtersearch_view'),
]
