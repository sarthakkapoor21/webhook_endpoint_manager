from collections import namedtuple

from django.db import models

from webhook_endpoint_manager.constants import CHAR_FIELD_LENGTHS


class Endpoint(models.Model):
    unique_url = models.CharField(max_length=CHAR_FIELD_LENGTHS.SHORT)
    base = models.CharField(max_length=CHAR_FIELD_LENGTHS.LONG, default='/')
    created_at = models.DateTimeField(auto_now_add=True)


class RequestData(models.Model):
    endpoint = models.ForeignKey(to=Endpoint, on_delete=models.CASCADE)
    raw_body = models.JSONField()


class RequestMetaData(models.Model):
    DATA_TYPE = namedtuple('DATA_TYPE', ['QUERY_PARAM', 'HEADER'])(
        QUERY_PARAM=1,
        HEADER=2,
    )

    DATA_TYPE_CHOICES = [
        (DATA_TYPE.QUERY_PARAM, 'Query Param'),
        (DATA_TYPE.HEADER, 'Header'),
    ]

    key = models.CharField(max_length=CHAR_FIELD_LENGTHS.LONG)
    value = models.CharField(max_length=CHAR_FIELD_LENGTHS.LONG)
    request = models.ForeignKey(to=RequestData, on_delete=models.CASCADE)
    data_type = models.PositiveSmallIntegerField(choices=DATA_TYPE_CHOICES)
