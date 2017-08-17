from django.test import TestCase

from apps.lesson.models import LessonSet, Lesson, Page


class LessonSetTestCase(TestCase):
    
    def setUp(self):
        LessonSet.objects.create(topic='topic 1')
        LessonSet.objects.create(topic='topic 2', description='description 2')

    def test_topic(self):
        lesson_set1 = LessonSet.objects.get(topic='topic 1')
        lesson_set2 = LessonSet.objects.get(topic='topic 2', description='description 2')
        self.assertEqual(lesson_set1.topic, 'topic 1')
        self.assertNotEqual(lesson_set1.topic, 'abracadabra')
        self.assertEqual(lesson_set2.topic, 'topic 2')
        self.assertEqual(lesson_set2.description, 'description 2')


class LessonTestCase(TestCase):
    
    def setUp(self):
        self.lesson_set1 = LessonSet.objects.create(topic='topic 1')
        self.lesson_set2 = LessonSet.objects.create(topic='topic 2', description='description 2')
        Lesson.objects.create(topic='topic 1', lesson_set=self.lesson_set1)
        Lesson.objects.create(topic='topic 2', description='description 2', lesson_set=self.lesson_set1)
        Lesson.objects.create(topic='topic 3', lesson_set=self.lesson_set2)

    def test_topic(self):
        lesson1 = Lesson.objects.get(topic='topic 1')
        lesson2 = Lesson.objects.get(topic='topic 2', description='description 2')
        self.assertEqual(lesson1.topic, 'topic 1')
        self.assertNotEqual(lesson1.topic, 'abracadabra')
        self.assertEqual(lesson2.topic, 'topic 2')
        self.assertEqual(lesson2.description, 'description 2')
        self.assertEqual(lesson1.lesson_set, self.lesson_set1)

    def test_relations(self):
        self.assertTrue(self.lesson_set1.lessons.all().count() > 1)
        self.assertTrue(self.lesson_set2.lessons.all().count() > 0)


class PageTestCase(TestCase):
    
    def setUp(self):
        self.lesson_set1 = LessonSet.objects.create(topic='topic 1')
        self.lesson_set2 = LessonSet.objects.create(topic='topic 2', description='description 2')
        self.lesson_1 = Lesson.objects.create(topic='topic 1', lesson_set=self.lesson_set1)
        self.lesson_2 = Lesson.objects.create(topic='topic 2', description='description 2', lesson_set=self.lesson_set1)
        self.lesson_3 = Lesson.objects.create(topic='topic 3', lesson_set=self.lesson_set2)
        page1 = Page.objects.create(text='text1', page_number=1, lesson=self.lesson_1)
        page2 = Page.objects.create(text='text2', page_number=2, lesson=self.lesson_1)
        page3 = Page.objects.create(text='text3', page_number=1, lesson=self.lesson_2)
        page4 = Page.objects.create(text='text4', page_number=1, lesson=self.lesson_3)

    def test_text(self):
        page1 = Page.objects.get(text='text1', page_number=1, lesson=self.lesson_1)
        page2 = Page.objects.get(text='text2', page_number=2, lesson=self.lesson_1)
        page3 = Page.objects.get(text='text3', page_number=1, lesson=self.lesson_2)
        page4 = Page.objects.get(text='text4', page_number=1, lesson=self.lesson_3)
        self.assertEqual(page1.text, 'text1')
        self.assertNotEqual(page1.text, 'abracadabra')
        self.assertEqual(page2.text, 'text2')
        self.assertEqual(page3.text, 'text3')
        self.assertEqual(page4.text, 'text4')

    def test_relations(self):
        self.assertTrue(self.lesson_set1.lessons.all().count() > 1)
        self.assertTrue(self.lesson_set2.lessons.all().count() > 0)
        self.assertTrue(self.lesson_1.pages.all().count() > 1)
        self.assertTrue(self.lesson_2.pages.all().count() > 0)
        self.assertTrue(self.lesson_3.pages.all().count() > 0)
