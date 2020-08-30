import random

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from polls.models import Choice, Question


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('user_name')


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
    question_text = factory.Faker('sentence')
    pub_date = timezone.now() + timezone.timedelta(random.randint(-10000, 10000))
    created_by = factory.SubFactory(UserFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice
    choice_text = factory.Faker('word')
    votes = factory.Faker('random_int')
    question = factory.SubFactory(QuestionFactory)
