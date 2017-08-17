from rest_framework import serializers

from apps.api.serializers.userprofile import UserSerializer
from apps.lesson.models import LessonSet, Lesson, Page, Favorite, LogLesson


class LessonSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonSet
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    page = PageSerializer()
    
    class Meta:
        model = Favorite
        fields = '__all__'


class LogLessonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    lesson = LessonSerializer()
    
    class Meta:
        model = LogLesson
        fields = '__all__'
