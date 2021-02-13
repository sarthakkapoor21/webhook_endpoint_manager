from django.contrib import admin, auth

from endpoints.models import Endpoint, RequestData, RequestMetaData

admin.site.register(Endpoint)
admin.site.register(RequestData)
admin.site.register(RequestMetaData)
admin.site.unregister(auth.models.Group)
