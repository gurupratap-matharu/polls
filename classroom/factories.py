import factory
from django.contrib.auth import get_user_model

from classroom.models import Classroom


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('user_name')


class ClassroomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Classroom
    name = factory.Faker('catch_phrase')
    section = factory.Faker('state_abbr')
    subject = factory.Faker('slug')
    room = factory.Faker('word')
    created_by = factory.SubFactory(UserFactory)
