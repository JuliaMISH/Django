from celery import shared_task
import time
import datetime
from .models import Post, Author, SubsUser, Category, PostCategory
from django.contrib.auth.models import User
from django.core.mail import send_mail



# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")

# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


# @shared_task
# def send_mail_after_post(post):
#     post_text = post.preview_mail()
#     post_category = PostCategory.objects.get(postThrough=post.id).categoryThrough
#     adress = []
#     for i in SubsUser.objects.filter(subsThrough=post_category.id):
#         adress.append(f'{i.userThrough.email}')  
#         send_mail(
#             subject=f'Hello!',
#             message=f"New article to read '{post.title}'! \n"
#                     f" text preview: {post_text} \n "
#                      f"link: https://testdjango-1.relyt2003.repl.co/news/{post.id}",
#             from_email='test-django-skill@yandex.ru',
#             recipient_list=adress
#             )

@shared_task
def send_mail_after_post(post_title, post_text, post_id, adress):
    send_mail(
        subject=f'Hello!',
        message=f"New article to read '{post_title}'! \n"
                f" text preview: {post_text} \n "
                f"link: https://testdjango-1.relyt2003.repl.co/news/{post_id}",
        from_email='test-django-skill@yandex.ru',
        recipient_list=adress
        )

@shared_task
def send_mail_weekly():
    # getting past week's posts
    posts_of_past_week = []
    for i in Post.objects.all():
        if f'{datetime.date.today() - i.dateCreation.date()}'.split(' ')[:1][0] == '0:00:00':
            posts_of_past_week.append(i)
        elif int(f'{datetime.date.today() - i.dateCreation.date()}'.split(' ')[:1][0]) < 8:
            posts_of_past_week.append(i)

    # forming text for email sending from posts_of_past_week
    posts_by_cat = {}
    for i in posts_of_past_week:
        post_category = PostCategory.objects.get(postThrough=i.id).categoryThrough.name
        if post_category in posts_by_cat.keys():
            posts_by_cat[f'{post_category}'] += f'\n Title: {i.title} | Text preview: {i.preview_mail()} | link: {i.post_link()}'
        else:
            posts_by_cat[f'{post_category}'] = f'Here are new posts for past week in {post_category}:'

    for i in posts_by_cat.keys():
        if posts_by_cat[i] == f'Here are new posts for past week in {i}:':
            posts_by_cat[i] = f'There is nothing new in {i} for past week :('

    # getting all subscribers
    subs = {}
    for i in SubsUser.objects.all():
        email = i.userThrough.email
        category = i.subsThrough.name
        if f'{email}' in subs.keys():
            subs[f'{email}'].append(f'{category}')
        else:
            subs[f'{email}'] = [f'{category}', ]

    # sending mails to subscribers
    for i in subs.keys():
        user = User.objects.get(email=i).username
        text = f'Dear {user}!'
        for j in subs[i]:
            text += f'\n {posts_by_cat[j]}'
        send_mail(
            subject=f'Hello, {user}! New articles to read:)',
            message=text,
            from_email='test-django-skill@yandex.ru',
            recipient_list=[i, ]
        )
