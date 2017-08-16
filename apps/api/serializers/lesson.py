from rest_framework import serializers

from apps.lesson.models import LessonSet, Lesson, Page


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
