from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author, PostCategory, SubsUser, Category
from django.forms import widgets
from django.contrib.auth.models import User

# создаём фильтр
class PostFilter(FilterSet):
    date = DateFilter(
        field_name="dateCreation",
        lookup_expr="gt",
        label="Дата",
        widget=widgets.TextInput(attrs={"type": "date"}))


    date.field.error_messages = {'invalid': 'Введите дату в формате ДД.ММ.ГГГГ. Например 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'ДД.ММ.ГГГГ'}
    #title = ModelChoiceFilter(queryset=Post.objects.all(), label="Заголовок")
    #title = CharFilter(lookup_expr='icontains', label="Заголовок")
    author = ModelChoiceFilter(queryset=Author.objects.all(), label="Автор")
    postCategory = ModelChoiceFilter(queryset=Category.objects.all(), label="Категория")

    # в мета классе предоставляем модель и указываем поля, по которым будет фильтроваться информация
    class Meta:
        model = Post
        fields = ('author', 'postCategory', 'date')

class CategoryFilter(FilterSet):
    user = ModelChoiceFilter(queryset=User.objects.all(), label="Пользователь")
    postCategory = ModelChoiceFilter(queryset=PostCategory.objects.all(), label="Категория")
    #category = ModelChoiceFilter(queryset=PostCategory.objects.all(), label="Категория")

    # в мета классе предоставляем модель и указываем поля, по которым будет фильтроваться информация
    class Meta:
        model = SubsUser
        fields = ('user', 'postCategory')