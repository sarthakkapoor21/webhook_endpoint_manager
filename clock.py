from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    from endpoints import models as endpoints_models
    endpoints_models.Endpoint.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=1)).delete()


scheduler.start()
