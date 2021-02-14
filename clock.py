from datetime import datetime, timedelta

import django

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
django.setup(set_prefix=False)


@scheduler.scheduled_job('interval', minutes=1)
def delete_hour_old_endpoints():
    print('THIS RUNS EVERY MINUTE TO DELETE HOUR OLD ENDPOINTS\n')
    from endpoints import models as endpoints_models
    endpoints_models.Endpoint.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=60)).delete()


scheduler.start()
