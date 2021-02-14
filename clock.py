from datetime import datetime, timedelta

import django

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
django.setup(set_prefix=False)

from endpoints import models as endpoints_models


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    print('THIS RUNS EVERY MINUTE\n')
    endpoints_models.Endpoint.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=1)).delete()


scheduler.start()
