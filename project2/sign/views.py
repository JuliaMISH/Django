from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

    # def form_valid(self, form):
    #     user = form.save()
    #     print(user)
        # post_text = post.preview_mail()
        # post_category = PostCategory.objects.get(postThrough=post.id).categoryThrough
        # # print(f'-----{a.title}------')
        # adress = []
        # for i in SubsUser.objects.filter(subsThrough=post_category.id):
        #     adress.append(f'{i.userThrough.email}')
        # # print(adress) #post.author, post.title, post.categoryType, SubsUser.objects.filter(subsThrough)
        #
        # send_mail(
        #     subject=f'Hello!',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=f"New article to read '{post.title}'! \
        #   {post_text}",  # сообщение с кратким описанием проблемы
        #     from_email='test-django-skill@yandex.ru',
        #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=adress
        # )
        # return super().form_valid(form)

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')