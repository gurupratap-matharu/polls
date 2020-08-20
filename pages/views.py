from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from pages.forms import ContactForm, FeedbackForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class ContactPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/contact.html'
    success_message = 'Thanks! We have received your message!'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/feedback.html'
    success_message = 'Thanks! We have received your feedback!'
    form_class = FeedbackForm
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
