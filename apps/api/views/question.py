from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.serializers.question import QuestionSerializer, AnswerSerializer
from apps.question.models import Question, Answer


class QuestionViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
