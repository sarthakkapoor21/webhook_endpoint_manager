from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from endpoints import models as endpoints_models

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    endpoints_models.Endpoint.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=1)).delete()


scheduler.start()
