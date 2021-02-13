from rest_framework.serializers import ModelSerializer, Serializer

from endpoints.models import Endpoint, RequestData, RequestMetaData


class RequestMetaDataSerializer(ModelSerializer):

    class Meta(object):
        model = RequestMetaData
        fields = ['key', 'value']


class RequestDataSerializer(ModelSerializer):

    query_params = RequestMetaDataSerializer(many=True)
    headers = RequestMetaDataSerializer(many=True)

    class Meta(object):
        model = RequestData
        fields = '__all__'


class EndpointBaseSerializer(ModelSerializer):

    class Meta(object):
        model = Endpoint
        fields = '__all__'


class EndpointDetailSerializer(ModelSerializer):

    request_data = RequestDataSerializer(many=True)

    class Meta(object):
        model = Endpoint
        fields = '__all__'
