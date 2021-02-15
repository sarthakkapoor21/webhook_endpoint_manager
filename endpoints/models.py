import uuid
from collections import namedtuple

from django.db import models

from webhook_endpoint_manager.constants import CHAR_FIELD_LENGTHS


class Endpoint(models.Model):
    """
    Model to Save Endpoint.
    unique_url: saves the unique_url of Endpoint.
    base: different base can be set in future (Base can be used to append before endpoint [FUTURE SCOPE])
    created_at: time when Endpoint is created.
    """
    unique_url = models.UUIDField(default=uuid.uuid4, editable=False)
    base = models.CharField(max_length=CHAR_FIELD_LENGTHS.LONG, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}/{} - {}'.format(self.base, self.unique_url, self.created_at)


class RequestData(models.Model):
    """
    Model to save Request Data for a particular Endpoint.
    """
    endpoint = models.ForeignKey(to=Endpoint, on_delete=models.CASCADE, related_name='request_data')
    raw_body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}/{} - {}'.format(self.endpoint.base, self.endpoint.unique_url, self.created_at)


class RequestMetaData(models.Model):
    """
    Model to save Query Params or Headers for a Particular Request
    """
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
    request = models.ForeignKey(to=RequestData, on_delete=models.CASCADE, related_name='meta_data')
    data_type = models.PositiveSmallIntegerField(choices=DATA_TYPE_CHOICES)

    def __str__(self):
        return '{}: {} - {}'.format(self.key, self.value, self.request)
