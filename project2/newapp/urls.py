from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostFil, PostCreateView, PostUpdateView, PostDeleteView, ProfileUpdateView, SubsCreateView, enough_view, CeleryTestView
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(PostsList.as_view())),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view())),
   path('search/', PostFil.as_view()),
   path('add/', PostCreateView.as_view(), name='post_create'),
   path('edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
   path('profile/', ProfileUpdateView.as_view(), name='profile'),
   #path('profile/', ProfileView.as_view(), name='profile'),
   path('subscribe/', SubsCreateView.as_view(), name='subscribe'),
   path('enough/', enough_view, name='enough'),
   path('celery/', CeleryTestView.as_view(), name='celery'),

]