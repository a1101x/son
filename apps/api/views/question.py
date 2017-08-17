from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from apps.api.serializers.question import QuestionSerializer, AnswerSerializer, UserAnswerSerializer
from apps.question.models import Question, Answer, UserAnswer
from apps.userprofile.models import User


class QuestionViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    @detail_route(methods=['post'], url_path='answer')
    def answer(self, request, pk=None):
        question = self.get_object()
        answers = request.data.get('answers', None)

        if answers:
            right_answers = question.answers.filter(is_valid=True)
            print(right_answers)

        return Response(QuestionSerializer(question).data)


class AnswerViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class UserAnswerViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = UserAnswerSerializer
    
    def get_queryset(self):
        queryset = UserAnswer.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user = User.objects.get(id=request.data['user'])
            question = Question.objects.get(id=request.data['question'])
            user_answer = UserAnswer(user=user, question=question)
            user_answer.clean()
            user_answer.save()

        serializer = UserAnswerSerializer(user_answer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
