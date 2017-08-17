import os

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save 
from django.dispatch import receiver

from apps.userprofile.models import User


def page_upload_to(instance, filename):
    return os.path.join('pages', filename)

def lesson_upload_to(instance, filename):
    return os.path.join('lessons', filename)

def lesson_set_upload_to(instance, filename):
    return os.path.join('lesson_sets', filename)


class LessonInfo(models.Model):
    topic = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} - {}'.format(self.topic, self.description[:120] + '...' if self.description else '')


class LessonSet(LessonInfo):
    image = models.ImageField(upload_to=lesson_set_upload_to, null=True, blank=True, height_field='height_field',
                              width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    file = models.FileField(upload_to=lesson_set_upload_to, null=True, blank=True)


class Lesson(LessonInfo):
    image = models.ImageField(upload_to=lesson_upload_to, null=True, blank=True, height_field='height_field',
                              width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    file = models.FileField(upload_to=lesson_upload_to, null=True, blank=True)
    lesson_set = models.ForeignKey(LessonSet, related_name='lessons')


class Page(models.Model):
    text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=page_upload_to, null=True, blank=True, height_field='height_field',
                              width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    file = models.FileField(upload_to=page_upload_to, null=True, blank=True)
    page_number = models.PositiveIntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name='pages')

    def __str__(self):
        return '{} - {}'.format(self.page_number, self.text[:120] + '...' if self.text else '')

    class Meta:
        ordering = ('page_number',)


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites')
    page = models.ForeignKey(Page)

    def __str__(self):
        return '{} - {}'.format(self.user, self.page)


class LogLesson(models.Model):
    user = models.ForeignKey(User, related_name='viewed_lesson')
    lesson = models.ForeignKey(Lesson)
    is_viewed = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.lesson, self.is_viewed)
