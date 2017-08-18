from django.conf.urls import url
from django.contrib import admin

from apps.userprofile.views import SedAppForm, BlockUserView, DownloadAppView


urlpatterns = [
    url(r'^send-app/(?P<email>[\w.@+-]+)/(?P<device>[\w.@+-]+)/$', SedAppForm.as_view(), name='send_app'),
    url(r'^download-app/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<device>[\w.@+-]+)/$', DownloadAppView.as_view(), 
        name='download_app'),
    url(r'^block-user/(?P<email>[\w.@+-]+)/$', BlockUserView.as_view(), name='block_user'),
]
