from django.urls import path, reverse_lazy
from . import views

app_name='cfis'
urlpatterns = [
    path('', views.HomeView.as_view()),
    path('news', views.NewsListView.as_view(), name='all'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/create',
        views.NewsCreateView.as_view(success_url=reverse_lazy('ads:all')), name='news_create'),
    path('news/<int:pk>/update',
        views.NewsUpdateView.as_view(success_url=reverse_lazy('ads:all')), name='news_update'),
    path('news/<int:pk>/delete',
        views.NewsDeleteView.as_view(success_url=reverse_lazy('ads:all')), name='news_delete'),
    path('news/<int:pk>', views.stream_file, name='news_picture'),
    path('news/<int:pk>/comment',
        views.NewsCommentCreateView.as_view(), name='news_comment_create'),
    path('comment/<int:pk>/delete',
        views.NewsCommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='news_comment_delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
