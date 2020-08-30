from django.contrib.auth import get_user_model
from django.test import TestCase

from classroom.factories import ClassroomFactory, UserFactory
from classroom.models import Classroom


class ClassroomModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.classroom = Classroom.objects.create(
            name='test_class',
            section='test_section',
            subject='test_subject',
            room='test_room',
            created_by=self.user
        )

    def test_classroom_listing(self):
        self.assertEqual(f'{self.classroom.name}', 'test_class')
        self.assertEqual(f'{self.classroom.section}', 'test_section')
        self.assertEqual(f'{self.classroom.subject}', 'test_subject')
        self.assertEqual(f'{self.classroom.room}', 'test_room')
        self.assertEqual(self.classroom.created_by, self.user)
        self.assertEqual(str(self.classroom), 'test_class')


class ClassroomTests(TestCase):
    def test_classroom_model_creation(self):
        user = UserFactory()
        c1 = ClassroomFactory(name='Astrophysics', created_by=user)
        c2 = ClassroomFactory(name='Gravitational Mechanics', created_by=user)

        self.assertEqual(Classroom.objects.count(), 2)
        self.assertEqual(c1.created_by, user)
        self.assertEqual(c2.created_by, user)
        self.assertEqual(c1.name, 'Astrophysics')
        self.assertEqual(c2.name, 'Gravitational Mechanics')
