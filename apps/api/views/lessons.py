from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.serializers.lesson import LessonSetSerializer, LessonSerializer, PageSerializer
from apps.lesson.models import LessonSet, Lesson, Page


class LessonSetViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LessonSetSerializer
    queryset = LessonSet.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class PageViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()
