from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from .models import Post, Author, SubsUser, Category, PostCategory
from .filters import PostFilter, CategoryFilter
from .forms import PostForm, UserForm, SubscribeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.views import View
from .tasks import send_mail_after_post #hello, printer, 
from django.core.cache import cache

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 4  # поставим постраничный вывод в один элемент

    # def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
    #     return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        author = request.POST['author']
        categoryType = request.POST['categoryType']
        #dateCreation = request.POST['dateCreation']
        title = request.POST['title']
        text = request.POST['text']
        post = Post(author=author, categoryType=categoryType, title=title, text=text)
        post.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs): 
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
 
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        
        return obj


class PostFil(PostsList):
    template_name = 'postfilter.html'
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

    #тут будет жить подписка


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newapp.add_post')
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    success_url = '/news/add/'

    def form_valid(self, form):
        post = form.save(commit=False)
        curr_date = datetime.date.today()
        posts_today = []
        # print(f'today: {today}')
        for i in Post.objects.filter(author=post.author):
            if i.dateCreation.date() == curr_date:
                posts_today.append(i)
        print(len(posts_today))  # '[:10]==today
        # print(Post.objects.filter(author=self.author, dateCreation=today))
        if len(posts_today) > 2:
            return HttpResponseRedirect('/news/enough/') #https://testdjango-1.relyt2003.repl.co/news/
        else:
            form.save()
            post_id = post.id
            post_title = post.title
            post_text = post.preview_mail()
            post_category = PostCategory.objects.get(postThrough=post.id).categoryThrough
            adress = []
            for i in SubsUser.objects.filter(subsThrough=post_category.id):
                adress.append(f'{i.userThrough.email}')
            # send_mail_after_post.apply_async(args=(post_title, post_text, post_id, adress))
            send_mail_after_post.delay(post_title, post_text, post_id, adress)
            # post_text = post.preview_mail()
            # post_category = PostCategory.objects.get(postThrough=post.id).categoryThrough
            # # print(f'-----{a.title}------')
            # adress = []
            # for i in SubsUser.objects.filter(subsThrough=post_category.id):
            #     adress.append(f'{i.userThrough.email}')
            # # print(adress) #post.author, post.title, post.categoryType, SubsUser.objects.filter(subsThrough)

            # send_mail(
            #     subject=f'Hello!',
            #     # имя клиента и дата записи будут в теме для удобства
            #     message=f"New article to read '{post.title}'! \n"
            #             f" text preview: {post_text} \n "
            #             f"link: https://testdjango-1.relyt2003.repl.co/news/{post.id}",  # сообщение с кратким описанием проблемы
            #     from_email='test-django-skill@yandex.ru',
            #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
            #     recipient_list=adress
            # )
            return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save()
    #     post_text = post.preview_mail()
    #     post_category = PostCategory.objects.get(postThrough=post.id).categoryThrough
    #     # print(f'-----{a.title}------')
    #     adress = []
    #     for i in SubsUser.objects.filter(subsThrough=post_category.id):
    #         adress.append(f'{i.userThrough.email}')
    #     # print(adress) #post.author, post.title, post.categoryType, SubsUser.objects.filter(subsThrough)
    #
    #     send_mail(
    #         subject=f'Hello!',
    #         # имя клиента и дата записи будут в теме для удобства
    #         message=f"New article to read '{post.title}'! \
    #       {post_text}",  # сообщение с кратким описанием проблемы
    #         from_email='test-django-skill@yandex.ru',
    #         # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #         recipient_list=adress
    #     )
    #     return super().form_valid(form)

# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):   #вместо текущего миксина там стоял LoginRequiredMixin
    permission_required = ('newapp.change_post')
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    success_url = '/news/'


    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('newapp.delete_post')
    template_name = 'newapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/protected_profile.html'
    queryset = Author.objects.all()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'newapp/protected_profile.html'
    form_class = UserForm
    success_url = '/news/profile/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        return self.request.user


class SubsCreateView(CreateView):
    template_name = 'newapp/subscribe.html'
    form_class = SubscribeForm
    success_url = '/news/subscribe/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.userThrough = self.request.user
        return super().form_valid(form)

def enough_view(request, *args, **kwargs):
    return render(request, 'newapp/enough.html', {})


class CeleryTestView(View):
    def get(self, request):
        printer.apply_async([10], countdown = 5)
        hello.delay()
        return HttpResponse('Hello!')