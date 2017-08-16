from django.test import TestCase

from apps.question.models import Question, Answer


class QuestionTestCase(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(question_text='question test')
        self.question2 = Question.objects.create(question_text='another question test', is_published=True)

    def test_text(self):
        self.assertEqual(self.question1.question_text, 'question test')
        self.assertNotEqual(self.question1.question_text, 'abracadabra')
        self.assertEqual(self.question2.question_text, 'another question test')
    
    def test_is_blocked(self):
        self.assertFalse(self.question1.is_published)
        self.assertTrue(self.question2.is_published)


class AnswerTestCase(TestCase):
    def setUp(self):
        question1 = Question.objects.create(question_text='question test')
        question2 = Question.objects.create(question_text='another question test', is_published=True)
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
