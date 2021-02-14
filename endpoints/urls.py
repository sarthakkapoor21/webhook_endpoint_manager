from django.conf.urls import url

from rest_framework import routers

from endpoints import (
    views as endpoints_views,
)

router = routers.SimpleRouter()
router.register(r'', endpoints_views.EndpointViewSet, basename='Endpoint')
urlpatterns = [
    url(
        regex=r'^(?P<endpoint_unique_url>[\-_a-zA-Z0-9]+)/save-request-data/$',
        view=endpoints_views.EndpointRequestView.as_view(),
        name="endpoint_request"
    ),
] + router.urls
