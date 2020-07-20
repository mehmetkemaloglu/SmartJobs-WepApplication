from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .Recommendation import ScheduledJob


class JobsapiConfig(AppConfig):
    name = 'jobsApi'

    def ready(self):
        sch = BackgroundScheduler()
        sch.add_job(ScheduledJob.start, trigger='cron', hour='3', minute='30')
        sch.start()


