from django.conf.urls import url, include
from rest_framework import routers

from apps.api.views.lessons import LessonSetViewSet, LessonViewSet, PageViewSet, FavoriteViewSet
from apps.api.views.question import QuestionViewSet, AnswerViewSet, UserAnswerViewSet
from apps.api.views.userprofile import UserViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='user'),
router.register(r'lesson_set', LessonSetViewSet, base_name='lesson_set')
router.register(r'lesson', LessonViewSet, base_name='lesson')
router.register(r'page', PageViewSet, base_name='page')
router.register(r'favorite', FavoriteViewSet, base_name='favorite')
router.register(r'question', QuestionViewSet, base_name='question')
router.register(r'answer', AnswerViewSet, base_name='answer')
router.register(r'user_answer', UserAnswerViewSet, base_name='user_answer')

urlpatterns = [
    url(r'^', include(router.urls)),
]
