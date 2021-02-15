from datetime import datetime, timedelta

from django.db.models import Count, Prefetch

from rest_framework import (
    generics as drf_generics,
    mixins as drf_mixins,
    response as drf_response,
    viewsets as drf_viewsets,
)

from endpoints import (
    models as endpoints_models,
    serializers as endpoints_serializers,
)


class EndpointViewSet(
    drf_mixins.CreateModelMixin, drf_mixins.ListModelMixin, drf_mixins.RetrieveModelMixin, drf_viewsets.GenericViewSet,
):
    """
    This is the Endpoint ViewSet.
    This is used to show List of Endpoints, Show Detail of Particular Endpoint, Create New Endpoint
    """
    serializer_class = endpoints_serializers.EndpointListSerializer
    model = endpoints_models.Endpoint
    lookup_field = 'unique_url'

    def get_serializer_class(self):
        serializer_class = endpoints_serializers.EndpointListSerializer
        if self.action == 'retrieve':
            serializer_class = endpoints_serializers.EndpointDetailSerializer
        return serializer_class

    def get_queryset(self):
        queryset = endpoints_models.Endpoint.objects.prefetch_related('request_data').annotate(
            request_count=Count('request_data')
        ).all().order_by('created_at')
        if self.action == 'retrieve':
            # If we want to get Detail of a particular Endpoint.
            # We prefetch Request Data, Query Params, Headers
            # Also we show Hits that happened in the last 5 minutes
            queryset = endpoints_models.Endpoint.objects.prefetch_related(
                Prefetch(
                    'request_data',
                    queryset=endpoints_models.RequestData.objects.filter(
                        created_at__gte=datetime.now() - timedelta(minutes=5)
                    ),
                ),
                Prefetch(
                    'request_data__meta_data',
                    queryset=endpoints_models.RequestMetaData.objects.filter(
                        data_type=endpoints_models.RequestMetaData.DATA_TYPE.QUERY_PARAM
                    ),
                    to_attr='query_params',
                ),
                Prefetch(
                    'request_data__meta_data',
                    queryset=endpoints_models.RequestMetaData.objects.filter(
                        data_type=endpoints_models.RequestMetaData.DATA_TYPE.HEADER
                    ),
                    to_attr='headers',
                )
            )
        return queryset


class EndpointRequestView(drf_generics.CreateAPIView):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Whenever a POST request is made on the endpoint, we save the data, headers, and query_params.
        """
        try:
            request_object_id = endpoints_models.RequestData.objects.create(
                endpoint=endpoints_models.Endpoint.objects.get(unique_url=kwargs['endpoint_unique_url']),
                raw_body=request.data
            ).id
            request_meta_data_objects_to_create = []
            # Save all the Headers
            for key, value in request.headers.items():
                request_meta_data_objects_to_create.append(
                    endpoints_models.RequestMetaData(
                        key=key,
                        value=value,
                        request_id=request_object_id,
                        data_type=endpoints_models.RequestMetaData.DATA_TYPE.HEADER
                    )
                )
            # Save all the Query Params
            for key, value_list in dict(request.GET).items():
                for value in value_list:
                    request_meta_data_objects_to_create.append(
                        endpoints_models.RequestMetaData(
                            key=key,
                            value=value,
                            request_id=request_object_id,
                            data_type=endpoints_models.RequestMetaData.DATA_TYPE.QUERY_PARAM
                        )
                    )
            endpoints_models.RequestMetaData.objects.bulk_create(request_meta_data_objects_to_create)
        except endpoints_models.Endpoint.DoesNotExist:
            pass
        return drf_response.Response()
