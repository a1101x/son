from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.serializers.lesson import LessonSetSerializer, LessonSerializer, PageSerializer, FavoriteSerializer
from apps.lesson.models import LessonSet, Lesson, Page, Favorite
from apps.userprofile.models import User


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
