from rest_framework import (
    fields as drf_fields,
    serializers as drf_serializers,
)

from endpoints.models import Endpoint, RequestData, RequestMetaData


class RequestMetaDataSerializer(drf_serializers.ModelSerializer):

    class Meta(object):
        model = RequestMetaData
        fields = ['key', 'value']


class RequestDataSerializer(drf_serializers.ModelSerializer):

    query_params = RequestMetaDataSerializer(many=True)
    headers = RequestMetaDataSerializer(many=True)

    class Meta(object):
        model = RequestData
        fields = '__all__'


class EndpointBaseSerializer(drf_serializers.ModelSerializer):

    request_count = drf_fields.CharField(read_only=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'


class EndpointDetailSerializer(drf_serializers.ModelSerializer):

    request_data = RequestDataSerializer(many=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'
