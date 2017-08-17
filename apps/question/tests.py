from django.test import TestCase

from apps.lesson.models import LessonSet, Lesson
from apps.question.models import Question, Answer, UserAnswer
from apps.userprofile.models import User


class QuestionTestCase(TestCase):
    
    def setUp(self):
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.question1 = Question.objects.create(question_text='question test', lesson=self.lesson)
        self.question2 = Question.objects.create(question_text='another question test', is_published=False, 
                                                 lesson=self.lesson)

    def test_text(self):
        self.assertEqual(self.question1.question_text, 'question test')
        self.assertNotEqual(self.question1.question_text, 'abracadabra')
        self.assertEqual(self.question2.question_text, 'another question test')
    
    def test_is_blocked(self):
        self.assertTrue(self.question1.is_published)
        self.assertFalse(self.question2.is_published)


class AnswerTestCase(TestCase):
    
    def setUp(self):
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        question1 = Question.objects.create(question_text='question test', lesson=self.lesson)
        question2 = Question.objects.create(question_text='another question test', is_published=True, 
                                            lesson=self.lesson)
        self.answer1 = Answer.objects.create(text='answer text', question=question1, is_valid=True)
        self.answer2 = Answer.objects.create(text='some answer text', question=question1, is_active=False)
        self.answer3 = Answer.objects.create(text='yet another answer text', question=question2, is_active=False)

    def test_text(self):
        self.assertEqual(self.answer1.text, 'answer text')
        self.assertNotEqual(self.answer1.text, 'abracadabra')
        self.assertEqual(self.answer2.text, 'some answer text')
        self.assertEqual(self.answer3.text, 'yet another answer text')
    
    def test_is_valid_active(self):
        self.assertTrue(self.answer1.is_valid)
        self.assertTrue(self.answer1.is_active)
        self.assertFalse(self.answer2.is_valid)
        self.assertFalse(self.answer2.is_active)
        self.assertFalse(self.answer3.is_valid)
        self.assertFalse(self.answer3.is_active)


class UserAnswerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='passwd')
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.question = Question.objects.create(question_text='some random text', is_published=True, 
                                                lesson=self.lesson)
        self.question2 = Question.objects.create(question_text='another some random text', is_published=True, 
                                                 lesson=self.lesson)
        self.answer = Answer.objects.create(text='answer text', is_valid=True, is_active=True, question=self.question)
        self.user_answer1 = UserAnswer.objects.create(user=self.user, question=self.question, correct=True)
        self.user_answer2 = UserAnswer.objects.create(user=self.user, question=self.question2, correct=False)

    def test_user_answer(self):
        self.assertTrue(self.user_answer1.correct)
        self.assertFalse(self.user_answer2.correct)
        self.assertNotEqual(self.user_answer1.question, self.user_answer2.question)
