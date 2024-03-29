from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
#import wix_tracker.automatic_emails

# Default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wix_tracker.settings')

app = Celery('wix_tracker')

# Using a string here eliminates the need to serialize 
# the configuration object to child processes by the Celery worker.

# - namespace='CELERY' means all celery-related configuration keys
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django applications.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
    
app.conf.beat_schedule = {
    #Scheduler Name
    'send_automated_emails-d': {
        'task': 'send_automated_emails',
        'schedule': crontab(hour=11, minute=0),
    },
}  