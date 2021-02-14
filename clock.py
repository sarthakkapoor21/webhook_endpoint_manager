from datetime import datetime, timedelta

import django

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
django.setup(set_prefix=False)


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    from endpoints import models as endpoints_models
    endpoints_models.Endpoint.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=1)).delete()


scheduler.start()
