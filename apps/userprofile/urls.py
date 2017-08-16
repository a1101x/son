from django.conf.urls import url
from django.contrib import admin

from apps.userprofile.views import SendAndroidView, SendIOSView, BlockUserView


urlpatterns = [
    url(r'^send-android/(?P<email>[\w.@+-]+)/$', SendAndroidView.as_view(), name='send_android'),
    url(r'^send-ios/(?P<email>[\w.@+-]+)/$', SendIOSView.as_view(), name='send_ios'),
    url(r'^block-user/(?P<email>[\w.@+-]+)/$', BlockUserView.as_view(), name='block_user'),
]
