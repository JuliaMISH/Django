from django.urls import path, include
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:id>', ArticleDetailView.as_view(), name='article-detail'), #if in view 1st way is choosen? then use "pk" in link, if 2nd - then use 'id'
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:id>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]