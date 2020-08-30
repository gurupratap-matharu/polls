from django.core import mail
from django.test import TestCase

from pages.forms import ContactForm, FeedbackForm


class ContactFormTests(TestCase):
    def test_valid_contact_form_sends_email(self):
        form = ContactForm({
            'name': 'Luke Skywalker',
            'message': 'Love your website!'
        })
        self.assertTrue(form.is_valid())
        with self.assertLogs('pages.forms', level='INFO') as cm:
            form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_form_does_not_sends_email(self):
        form = ContactForm({
            'message': 'Love your website!'
        })
        self.assertFalse(form.is_valid())


class FeedbackFormTests(TestCase):
    def test_valid_feedback_form_sends_email(self):
        form = FeedbackForm({
            'name': 'Luke Skywalker',
            'message': 'Love your website!'
        })
        self.assertTrue(form.is_valid())
        with self.assertLogs('pages.forms', level='INFO') as cm:
            form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_feedback_form_does_not_sends_email(self):
        form = FeedbackForm({
            'message': 'Love your website!'
        })
        self.assertFalse(form.is_valid())
