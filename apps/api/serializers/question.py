from rest_framework import serializers

from apps.api.serializers.userprofile import UserSerializer
from apps.question.models import Question, Answer, UserAnswer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    question = QuestionSerializer()
    
    class Meta:
        model = UserAnswer
        fields = '__all__'
