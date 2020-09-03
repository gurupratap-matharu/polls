import logging

from django import forms
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EnrollmentForm(forms.Form):
    code = forms.UUIDField(label='Class Code')

    def send_mail(self, **kwargs):
        user_email = kwargs['student'].email
        logger.info('sending enrollment email to %s ...', user_email)
        message = 'Congratulations you have enrolled to class {} successfully!'.format(kwargs['classroom'].name)
        send_mail(subject='Site message', message=message, from_email='site@website.domain',
                  recipient_list=['gurupratap.matharu@gmail.com', user_email], fail_silently=False)
