from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from classroom.models import Classroom
from classroom.views import ClassroomDetailView, ClassroomListView


class ClassroomListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_classroom_list_redirects_for_anonymous_or_logged_out_user(self):
        response = self.client.get(reverse('classroom_list'))
        no_response = self.client.get('/classrooms/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/classroom_list.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_list_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('classroom_list'))
        no_response = self.client.get('/classrooms/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/classroom_list.html')
        self.assertContains(response, 'Classroom')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_list_resolves_classroomlistview(self):
        view = resolve(reverse('classroom_list'))
        self.assertEqual(view.func.__name__, ClassroomListView.as_view().__name__)


class ClassroomDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.classroom = Classroom.objects.create(
            name='Testclass',
            created_by=self.user
        )

    def test_classroom_detail_redirects_for_anonymous_or_logged_out_user(self):
        response = self.client.get(self.classroom.get_absolute_url())
        no_response = self.client.get('/classroom/123456/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/classroom_detail.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_detail_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.classroom.get_absolute_url())
        no_response = self.client.get('/classroom/123456')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/classroom_detail.html')
        self.assertContains(response, self.classroom.name)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_list_resolves_classroomlistview(self):
        view = resolve(self.classroom.get_absolute_url())
        self.assertEqual(view.func.__name__, ClassroomDetailView.as_view().__name__)


class ClassroomCreateTests(TestCase):
    pass


class ClassroomUpdateTests(TestCase):
    pass


class ClassroomDeleteTests(TestCase):
    pass
