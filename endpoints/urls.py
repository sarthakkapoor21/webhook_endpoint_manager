from django.conf.urls import url

from rest_framework import routers

from endpoints import (
    views as endpoints_views,
)

router = routers.SimpleRouter()
router.register(r'', endpoints_views.EndpointViewSet, basename='Endpoint')
urlpatterns = router.urls + [
    url(
        regex=r'^(?P<endpoint_unique_url>[\-_a-zA-Z0-9]+)/$',
        view=endpoints_views.EndpointRequestView.as_view(),
        name="endpoint_request"
    ),
]
