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
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    @detail_route(methods=['post'], url_path='answer')
    def answer(self, request, pk=None):
        question = self.get_object()
        answers = request.data.get('answer', None)

        if answers:
            right_answers = question.answers.filter(is_valid=True, is_active=True)

            if len(answers) != right_answers.count():
                user_answer = UserAnswer.objects.create(user=request.user, question=question, correct=False)
            else:
                if list(right_answers) == list(right_answers.filter(id__in=answers)):
                    user_answer = UserAnswer.objects.create(user=request.user, question=question, correct=True)
                else:
                    user_answer = UserAnswer.objects.create(user=request.user, question=question, correct=False)

        return Response(UserAnswerSerializer(user_answer).data)


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class UserAnswerViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
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
