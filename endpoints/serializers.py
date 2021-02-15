from datetime import datetime, timedelta

from rest_framework import (
    fields as drf_fields,
    serializers as drf_serializers,
)

from endpoints.models import Endpoint, RequestData, RequestMetaData


class RequestMetaDataSerializer(drf_serializers.ModelSerializer):
    """
    This is a serializer to return 'key' and 'value' of RequestMetaData Model for the Endpoint Detail Page
    This is used to show data for both Query Params and Headers
    """
    class Meta(object):
        model = RequestMetaData
        fields = ['key', 'value']


class RequestDataSerializer(drf_serializers.ModelSerializer):
    """
    This serializer is used to show data for Endpoint Detail Page.
    This shows all the fields of RequestData Model and also shows gets data for query_params and headers which are
    prefetched and are shown using RequestMetaDataSerializer
    """
    query_params = RequestMetaDataSerializer(many=True)
    headers = RequestMetaDataSerializer(many=True)

    class Meta(object):
        model = RequestData
        fields = '__all__'


class EndpointBaseSerializer(drf_serializers.ModelSerializer):
    """
    This is the Base Serializer for Endpoint List and Endpoint Detail Page
    """
    time_to_live = drf_fields.SerializerMethodField(read_only=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'

    def get_time_to_live(self, obj):
        """
        This function returns the time which is left in the endpoint being destroyed in minutes.
        Currently we're destroying the endpoints every hour.
        """
        return str((obj.created_at + timedelta(minutes=60) - datetime.now()).seconds // 60) + ' minutes to expire'


class EndpointListSerializer(EndpointBaseSerializer):
    """
    This is the Endpoint List serializer. It shows all the fields of Base Serializer + number of requests that each
    Endpoint has received (request_count).
    request_count is already fetched and annotated with the queryset.
    """
    request_count = drf_fields.CharField(read_only=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'


class EndpointDetailSerializer(EndpointBaseSerializer):
    """
    This Serializer is used on Endpoint Detail Page. This is used to show all Request Data for an Endpoint.
    """
    request_data = RequestDataSerializer(many=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'
