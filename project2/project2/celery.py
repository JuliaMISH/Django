import os
from celery import Celery
from celery.schedules import crontab

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
 
app = Celery('project2')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_weekly': {
        'task': 'newapp.tasks.send_mail_weekly',
        'schedule': crontab(), #hour=21, minute=31, day_of_week='thursday'
    },
}