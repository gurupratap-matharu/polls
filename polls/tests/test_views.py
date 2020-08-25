from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from polls.models import Question
from polls.views import (QuestionCreate, QuestionDelete, QuestionDetailView,
                         QuestionListView, QuestionUpdate)


class QuestionListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123',
        )
        self.question = Question.objects.create(
            question_text='When will I go to India?',
            pub_date=timezone.now()
        )

    def test_question_list_view_works_for_anonymous_user(self):
        response = self.client.get(reverse('polls:question_list'))
        no_response = self.client.get('/poll/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Polls')
        self.assertContains(response, 'Add')
        self.assertContains(response, 'Home')
        self.assertContains(response, self.question.question_text)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'polls/question_list.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_list_view_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('polls:question_list'))
        no_response = self.client.get('/poll/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Polls')
        self.assertContains(response, self.question.question_text)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'polls/question_list.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_list_view_resolve_questionlistview(self):
        view = resolve(reverse('polls:question_list'))
        self.assertEqual(view.func.__name__, QuestionListView.as_view().__name__)


class QuestionDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.question = Question.objects.create(
            question_text='When will I go to India?',
            pub_date=timezone.now()
        )

    def test_question_detail_view_works_for_anonymous_user(self):
        response = self.client.get(self.question.get_absolute_url())
        no_response = self.client.get('/polls/123456/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/question_detail.html')
        self.assertContains(response, 'Questions')
        self.assertContains(response, 'Polls')
        self.assertContains(response, self.question.question_text)
        self.assertNotContains(response, 'Hi. I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_question_detail_view_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.question.get_absolute_url())
        no_response = self.client.get('/polls/123456/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/question_detail.html')
        self.assertContains(response, 'Questions')
        self.assertContains(response, 'Polls')
        self.assertContains(response, self.question.question_text)
        self.assertNotContains(response, 'Hi. I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_question_detail_view_resolve_questiondetailview(self):
        view = resolve(self.question.get_absolute_url())
        self.assertEqual(view.func.__name__, QuestionDetailView.as_view().__name__)


class QuestionCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_question_create_view_redirects_for_anonymous_user(self):
        response = self.client.get(reverse('polls:question_create'))
        no_response = self.client.get('/poll/create/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'polls/question_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_create_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('polls:question_create'))
        no_response = self.client.get('/poll/create/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')
        self.assertContains(response, 'Question text')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'polls/question_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_create_resolve_questioncreateview(self):
        view = resolve(reverse('polls:question_create'))
        self.assertEqual(view.func.__name__, QuestionCreate.as_view().__name__)


class QuestionUpdateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.question = Question.objects.create(
            question_text='When will I go to India?',
            pub_date=timezone.now()
        )

    def test_question_update_view_redirects_for_anonymous_user(self):
        response = self.client.get(self.question.get_update_url())
        no_response = self.client.get('/poll/update/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'polls/question_update_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_update_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.question.get_update_url())
        no_response = self.client.get('/poll/update/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Question text')
        self.assertContains(response, self.question.question_text)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'polls/question_update_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_update_resolve_questionupdateview(self):
        view = resolve(self.question.get_update_url())
        self.assertEqual(view.func.__name__, QuestionUpdate.as_view().__name__)


class QuestionDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.question = Question.objects.create(
            question_text='When will I go to India?',
            pub_date=timezone.now()
        )

    def test_question_delete_redirects_for_anonymous_user(self):
        response = self.client.get(self.question.get_delete_url())
        no_response = self.client.get('/polls/123456/delete/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'polls/question_confirm_delete.html')
        self.assertEqual(no_response.status_code, 404)

    def test_question_delete_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.question.get_delete_url())
        no_response = self.client.get('/polls/123456/delete/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/question_confirm_delete.html')
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Confirm')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_question_delete_resolve_questiondeleteview(self):
        view = resolve(self.question.get_delete_url())
        self.assertEqual(view.func.__name__, QuestionDelete.as_view().__name__)
