import factory
from django.contrib.auth import get_user_model

from classroom.models import Classroom, Enrollment, Post


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


class EnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment
    student = factory.SubFactory(UserFactory)
    classroom = factory.SubFactory(ClassroomFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    title = factory.Faker('sentence')
    content = factory.Faker('text')
    created_on = factory.Faker('date_time_this_decade')

    author = factory.SubFactory(UserFactory)
    classroom = factory.SubFactory(ClassroomFactory)
