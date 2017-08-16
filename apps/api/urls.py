from django.conf.urls import url, include
from rest_framework import routers

from apps.api.views.lessons import LessonSetViewSet, LessonViewSet, PageViewSet
from apps.api.views.question import QuestionViewSet, AnswerViewSet
from apps.api.views.userprofile import UserViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='user'),
router.register(r'lesson_set', LessonSetViewSet, base_name='lesson_set')
router.register(r'lesson', LessonViewSet, base_name='lesson')
router.register(r'page', PageViewSet, base_name='page')
router.register(r'question', QuestionViewSet, base_name='question')
router.register(r'answer', AnswerViewSet, base_name='answer')
router.register(r'answer', AnswerViewSet, base_name='answer')

urlpatterns = [
    url(r'^', include(router.urls)),
]
