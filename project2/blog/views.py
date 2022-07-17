from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Article
from .forms import ArticleForm


class ArticleCreateView(CreateView):
    template_name = 'article/article_create2.html'
    form_class = ArticleForm
    queryset = Article.objects.all()
    #ways to redirect after successfull article creation:
    #1. using absolute url function in models (it is the way we did it here? so look into models)
    #2. using: success_url = '/'/ It should be written here in this class
    #3. using method( also should be written here in this class):
    #def get_success_url(self):
    #    return '\'



class ArticleListView(ListView):
    template_name = 'article/article_list2.html'
    queryset = Article.objects.all() # by default this generic-based view will search
    # template automatcally through next adress: <name of app in which it is used>/
    # <name of model in which it is used>_<name or type of the generic itself>.html
    # thus in our case it will search in templates/blog/article_list.html
    # becuase app is named "blog", model is named "Article' and generic is "ListView"

    # second way to show to django where to look for apropriate template:
    # template_name = '<name of folder inside template-folder of the app iself>/<temolate name>.html'
    # in our case it shoul be: template_name = 'article/article_list2.html'


class ArticleDetailView(DetailView):
    # it works like this:
    # template_name = 'article/article_detail2.html'
    # queryset = Article.objects.all()

    # or like this (for now we imagine that there is no difference btw theese two ways):
    template_name = 'article/article_detail2.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Article, id = id_)


class ArticleUpdateView(UpdateView):
    template_name = 'article/article_create2.html'
    form_class = ArticleForm
    queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Article, id = id_)


class ArticleDeleteView(DeleteView):
    template_name = 'article/article_delete2.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Article, id = id_)

    def get_success_url(self):
        return reverse('articles:article-list')