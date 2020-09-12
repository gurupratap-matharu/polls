import logging
import uuid

from django.core import mail
from django.test import TestCase

from classroom.factories import ClassroomFactory, UserFactory
from classroom.forms import EnrollmentForm, PostForm


class EnrollmentFormTests(TestCase):
    def test_valid_enrollment_form_with_new_enrollment_sends_email(self):
        student = UserFactory()
        classroom = ClassroomFactory()

        code = str(classroom.id)
        form = EnrollmentForm({'code': code})

        self.assertTrue(form.is_valid())

        with self.assertLogs('classroom.forms', level='INFO') as cm:
            form.send_mail(student=student, classroom=classroom)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_enrollment_form_does_not_sends_email(self):
        form = EnrollmentForm({'code': '123456'})
        self.assertFalse(form.is_valid())


class PostFormTests(TestCase):
    def test_valid_post_form_works(self):
        form = PostForm({'title': 'A new beginning', 'content': 'We have to start over again'})
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form = PostForm({'title': 'A new beginning'})
        self.assertFalse(form.is_valid())
