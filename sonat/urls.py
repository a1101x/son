from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)


urlpatterns = [
    url(r'^token-obtain/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^app/', include('apps.userprofile.urls', namespace='userprofile')),
    url(r'^api/', include('apps.api.urls', namespace='api')),
    url(r'', admin.site.urls),
]