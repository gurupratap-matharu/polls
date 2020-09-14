import uuid

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse

from classroom.factories import (ClassroomFactory, EnrollmentFactory,
                                 UserFactory)
from classroom.forms import EnrollmentForm, PostForm
from classroom.models import Classroom, Enrollment
from classroom.views import (ClassroomCreate, ClassroomDelete,
                             ClassroomDetailView, ClassroomListView,
                             ClassroomUpdate, EnrollmentCreate,
                             EnrollmentDelete)


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
        self.assertEqual(list(response.context['object_list']), list(Classroom.objects.all()))
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

    def test_classroom_detail_contains_post_model_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.classroom.get_absolute_url())

        self.assertIsInstance(response.context['form'], PostForm)

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


class EnrollmentCreateTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.classroom = ClassroomFactory(created_by=self.user)

    def test_enrollment_create_redirects_for_logged_out_user(self):
        response = self.client.get(reverse('enroll'))
        no_response = self.client.get('/enrollment/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/enrollment_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_enrollment_create_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('enroll'))
        no_response = self.client.get('/enrollment/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/enrollment_form.html')
        self.assertContains(response, 'Enroll')
        self.assertIsInstance(response.context['form'], EnrollmentForm)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_enrollment_create_resolves_enrollmentcreateview(self):
        view = resolve(reverse('enroll'))
        self.assertEqual(view.func.__name__, EnrollmentCreate.as_view().__name__)

    def test_code_for_non_existing_class_does_not_not_create_enrollment(self):
        code = uuid.uuid4()
        self.client.force_login(self.user)
        response = self.client.post(reverse('enroll'), data={'code': code})
        no_response = self.client.post('/enrollment/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Enrollment.objects.count(), 0)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(no_response.status_code, 404)

    def test_valid_enrollment_code_submission_works_correctly(self):
        code = str(self.classroom.id)
        self.client.force_login(self.user)
        response = self.client.post(reverse('enroll'), data={'code': code})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Enrollment.objects.count(), 1)

        enrollment = Enrollment.objects.all()[0]
        self.assertEqual(enrollment.classroom, self.classroom)
        self.assertEqual(enrollment.student, self.user)

    def test_valid_code_for_existing_class_creates_enrollment(self):
        code = str(self.classroom.id)

        request = self.factory.post(reverse('enroll'), data={'code': code})
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user

        response = EnrollmentCreate.as_view()(request)

        self.assertEqual(response.status_code, 302)

        enrollment = Enrollment.objects.all()[0]

        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(enrollment.student, self.user)
        self.assertEqual(enrollment.classroom, self.classroom)

    def test_valid_code_for_existing_enrollment_does_not_create_new_enrollment(self):
        code = str(self.classroom.id)
        _ = EnrollmentFactory(student=self.user, classroom=self.classroom)

        self.client.force_login(self.user)
        response = self.client.post(reverse('enroll'), data={'code': code})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertIn('You are already enrolled in', str(messages[0]))
        self.assertEqual(Enrollment.objects.count(), 1)


class EnrollmentDeleteTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.classroom = ClassroomFactory(created_by=self.user)
        self.enrollment = EnrollmentFactory(student=self.user,
                                            classroom=self.classroom)

    def test_enrollment_delete_redirects_for_logged_out_user(self):
        response = self.client.get(self.enrollment.get_delete_url())
        no_response = self.client.get('/enroll/1234/delete/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'classroom/enrollment_confirm_delete.html')
        self.assertEqual(no_response.status_code, 404)

    def test_enrollment_delete_view_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.enrollment.get_delete_url())
        no_response = self.client.get('/enroll/1234/delete/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/enrollment_confirm_delete.html')
        self.assertContains(response, 'Delete')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_enrollment_delete_resolves_enrollmentdeleteview(self):
        view = resolve(self.enrollment.get_delete_url())
        self.assertEqual(view.func.__name__, EnrollmentDelete.as_view().__name__)
