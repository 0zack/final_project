from django.urls import path, reverse_lazy
from . import views

app_name='cfis'
urlpatterns = [
    path('', views.HomeView.as_view()),
    path('news', views.NewsListView.as_view(), name='news_all'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/create',
        views.NewsCreateView.as_view(success_url=reverse_lazy('cfis:news_all')), name='news_create'),
    path('news/<int:pk>/update',
        views.NewsUpdateView.as_view(success_url=reverse_lazy('cfis:news_all')), name='news_update'),
    path('news/<int:pk>/delete',
        views.NewsDeleteView.as_view(success_url=reverse_lazy('cfis:news_all')), name='news_delete'),
    path('news_picture/<int:pk>', views.stream_file, name='news_picture'),
    path('news/<int:pk>/comment',
        views.NewsCommentCreateView.as_view(), name='news_comment_create'),
    path('news_comment/<int:pk>/delete',
        views.NewsCommentDeleteView.as_view(success_url=reverse_lazy('cfis')), name='news_comment_delete'),

    path('post', views.PostListView.as_view(), name='all'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create',
        views.PostCreateView.as_view(success_url=reverse_lazy('cfis:all')), name='post_create'),
    path('post/<int:pk>/update',
        views.PostUpdateView.as_view(success_url=reverse_lazy('cfis:all')), name='post_update'),
    path('post/<int:pk>/delete',
        views.PostDeleteView.as_view(success_url=reverse_lazy('cfis:all')), name='post_delete'),
    path('post_picture/<int:pk>', views.stream_file, name='post_picture'),
    path('post/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='post_favorite'),
    path('post/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='post_unfavorite'),
    path('post/<int:pk>/comment',
        views.PostCommentCreateView.as_view(), name='post_comment_create'),
    path('post_comment/<int:pk>/delete',
        views.PostCommentDeleteView.as_view(success_url=reverse_lazy('cfis')), name='post_comment_delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
