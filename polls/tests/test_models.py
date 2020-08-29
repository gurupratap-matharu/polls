from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from polls.models import Choice, Question


class QuestionModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.question = Question.objects.create(
            question_text='test_question',
            pub_date=timezone.now(),
            created_by=self.user
        )

    def test_question_listing(self):
        self.assertEqual(f'{self.question.question_text}', 'test_question')
        self.assertEqual(self.question.created_by, self.user)
        self.assertEqual(str(self.question), 'test_question')


class ChoiceModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.question = Question.objects.create(
            question_text='test_question',
            pub_date=timezone.now(),
            created_by=self.user

        )
        self.choice = Choice.objects.create(
            choice_text='test_choice',
            votes=2,
            question=self.question
        )

    def test_choice_listing(self):
        self.assertEqual(f'{self.choice.choice_text}', 'test_choice')
        self.assertEqual(self.choice.question, self.question)
