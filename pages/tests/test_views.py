from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from pages.views import (AboutPageView, ContactPageView, FeedbackPageView,
                         HomePageView)


class HomePageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_home_page_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pages:home'))
        no_response = self.client.get('/pages/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertContains(response, 'Home')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_home_page_works_for_anonymous_user(self):
        pass

    def test_home_page_resolves_homepageview(self):
        view = resolve(reverse('pages:home'))
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_about_page_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pages:about'))
        no_response = self.client.get('/pages/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertContains(response, 'About')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_about_page_works_for_anonymous_user(self):
        pass

    def test_about_page_resolve_aboutpageview(self):
        view = resolve(reverse('pages:about'))
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class ContactPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_contact_page_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pages:contact'))
        no_response = self.client.get('/pages/contact/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact.html')
        self.assertContains(response, 'Contact')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_contact_page_works_for_anonymous_user(self):
        pass

    def test_contact_page_resolve_contactpageview(self):
        view = resolve(reverse('pages:contact'))
        self.assertEqual(view.func.__name__, ContactPageView.as_view().__name__)


class FeedbackPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

    def test_feedback_page_works_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pages:feedback'))
        no_response = self.client.get('/pages/feedback/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/feedback.html')
        self.assertContains(response, 'Feedback')
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_feedback_page_works_for_anonymous_user(self):
        pass

    def test_feedback_page_resolves_feedbackpageview(self):
        view = resolve(reverse('pages:feedback'))
        self.assertEqual(view.func.__name__, FeedbackPageView.as_view().__name__)
