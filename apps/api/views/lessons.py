from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.serializers.lesson import LessonSetSerializer, LessonSerializer, PageSerializer, FavoriteSerializer, \
                                        LogLessonSerializer
from apps.lesson.models import LessonSet, Lesson, Page, Favorite, LogLesson
from apps.userprofile.models import User


class LessonSetViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LessonSetSerializer
    queryset = LessonSet.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    @detail_route(methods=['get'], url_path='copy')
    def copy(self, request, pk=None):
        lesson = self.get_object()
        lesson.id = None
        lesson.topic = lesson.topic + ' copy'
        lesson.save()
        return Response(LessonSerializer(lesson).data)

    @detail_route(methods=['post'], url_path='order')
    def order(self, request, pk=None):
        lesson = self.get_object()
        pages = request.data.get('pages', None)
        return Response(LessonSerializer(lesson).data)

    @detail_route(methods=['get'], url_path='pages')
    def pages(self, request, pk=None):
        lesson = self.get_object()
        pages = lesson.pages.all()
        return Response(PageSerializer(pages, many=True).data)


class PageViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class FavoriteViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = FavoriteSerializer
    
    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user = User.objects.get(id=request.data['user'])
            page = Page.objects.get(id=request.data['page'])

            try:
                favorite = Favorite.objects.get(user=user, page=page)
                favorite.delete()
            except Favorite.DoesNotExist:
                favorite = Favorite(user=user, page=page)
                favorite.clean()
                favorite.save()

        serializer = FavoriteSerializer(favorite)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LogLessonViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LogLessonSerializer
    queryset = LogLesson.objects.all()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user = User.objects.get(id=request.data['user'])
            lesson = Lesson.objects.get(id=request.data['lesson'])
            log_lesson = LogLesson(user=user, lesson=lesson)
            log_lesson.clean()
            log_lesson.save()

        serializer = LogLessonSerializer(log_lesson)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
