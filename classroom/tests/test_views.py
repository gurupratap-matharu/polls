from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from classroom.factories import ClassroomFactory, UserFactory
from classroom.models import Classroom
from classroom.views import (ClassroomCreate, ClassroomDelete,
                             ClassroomDetailView, ClassroomListView,
                             ClassroomUpdate)


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
    def setUp(self):
        self.user = UserFactory()
        self.classroom = ClassroomFactory(created_by=self.user)

    def test_classroom_create_view_redirects_for_anonymous_user(self):
        response = self.client.get(reverse('classroom_create'))
        no_response = self.client.get('/class/create/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/classroom_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_create_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('classroom_create'))
        no_response = self.client.get('/class/create/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')
        self.assertContains(response, 'name')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'classroom/classroom_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_create_resolve_classroomcreateview(self):
        view = resolve(reverse('classroom_create'))
        self.assertEqual(view.func.__name__, ClassroomCreate.as_view().__name__)


class ClassroomUpdateTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.classroom = ClassroomFactory(created_by=self.user)

    def test_classroom_update_view_redirects_for_anonymous_user(self):
        response = self.client.get(self.classroom.get_update_url())
        no_response = self.client.get('/class/update/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/classroom_update_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_update_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.classroom.get_update_url())
        no_response = self.client.get('/class/update/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update')
        self.assertContains(response, 'name')
        self.assertContains(response, self.classroom.name)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertTemplateUsed(response, 'classroom/classroom_update_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_update_resolve_classroomupdateview(self):
        view = resolve(self.classroom.get_update_url())
        self.assertEqual(view.func.__name__, ClassroomUpdate.as_view().__name__)


class ClassroomDeleteTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.classroom = ClassroomFactory(created_by=self.user)

    def test_classroom_delete_redirects_for_anonymous_user(self):
        response = self.client.get(self.classroom.get_delete_url())
        no_response = self.client.get('/classroom/123456/delete/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/classroom_confirm_delete.html')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_delete_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.classroom.get_delete_url())
        no_response = self.client.get('/classroom/123456/delete/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/classroom_confirm_delete.html')
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Confirm')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_classroom_delete_resolves_classroomdeleteview(self):
        view = resolve(self.classroom.get_delete_url())
        self.assertEqual(view.func.__name__, ClassroomDelete.as_view().__name__)
