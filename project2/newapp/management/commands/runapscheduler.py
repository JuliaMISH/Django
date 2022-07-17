import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from newapp.models import Post, SubsUser, PostCategory
import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# task for sending mails to subscribers
def my_job():
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
    # print('done')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="sun", hour="16", minute="01"),
            # second="*/20" То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")