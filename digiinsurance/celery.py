from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiinsurance.settings')

app = Celery('digiinsurance')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     # Run at end of day and early day to catch late payments
#     'check_for_payout': {
#         'task': 'tasks.cron.check_for_payouts',
#         'schedule': crontab(hour=4, minute=45)
#     },
#     'check_for_progress': {
#         'task': 'tasks.cron.check_for_progress',
#         'schedule': crontab(hour=16, minute=5)
#     },
#     'check_for_campaigns': {
#         'task': 'tasks.cron.check_for_campaigns',
#         'schedule': crontab(hour=16, minute=5)
#     },
#     'reset_emails_sent_today': {
#         'task': 'tasks.cron.reset_emails_sent_today',
#         'schedule': crontab(hour=16, minute=5)
#     },
#     'run_user_analytics_cron': {
#         'task': 'tasks.cron.run_user_analytics_cron',
#         'schedule': crontab(hour=16, minute=5)
#     }
# }


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
