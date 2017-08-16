from django.db import models

from apps.lesson.models import Lesson


class Question(models.Model):
    """
    Question's Model, which is used as question for lesson's
    """
    question_text = models.CharField(max_length=256, verbose_name='Question\'s text')
    is_published = models.BooleanField(default=True)
    lesson = models.ForeignKey(Lesson, related_name='questions')

    def __str__(self):
        return "{} - {} - {}".format(self.lesson, self.question_text, self.is_published)


class Answer(models.Model):
    """
    Answer's Model, which is used as the answer in Question Model
    """
    text = models.CharField(max_length=128, verbose_name='Answer\'s text')
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    question = models.ForeignKey(Question, related_name='answers')

    def __str__(self):
        return self.text
