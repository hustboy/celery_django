import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filemanager.settings')

app = Celery('filemanager')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
