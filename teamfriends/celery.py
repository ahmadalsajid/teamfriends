import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamfriends.settings')

app = Celery('teamfriends')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
