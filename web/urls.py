from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    AllUsers,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('likes/<int:post_pk>/', views.likes, name='likes'),
    path('dislikes/<int:post_pk>/', views.dislikes, name='dislikes'),
    path('add_comment/<int:post_pk>/', views.add_comment, name='add_comment'),
    path('comment_likes/<int:post_pk>/<int:comment_pk>', views.comment_likes, name='comment_likes'),
    path('comment_dislikes/<int:post_pk>/<int:comment_pk>', views.comment_dislikes, name='comment_dislikes'),
    path('comment_edit/<int:comment_pk>', views.comment_edit, name='comment_edit'),
    path('post/<int:post_pk>/upload/', views.image_upload_view, name='post-upload'),
    path('latest_posts/', views.latest_posts, name='latest_posts'),
    path('networks/', views.networks, name='networks'),
    path('image_delete/<int:pk>/', views.delete_image, name='image-delete'),
    path('all_users/', AllUsers.as_view(), name='all_users'),
    path('post_search', views.post_search, name='post_search'),
    path('calendar', views.calendar, name='calendar'),
]
