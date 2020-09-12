from django.contrib.auth import get_user_model
from django.test import TestCase

from classroom.factories import (ClassroomFactory, EnrollmentFactory,
                                 UserFactory)
from classroom.models import Classroom, Enrollment


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
        class_1 = ClassroomFactory(name='Astrophysics', created_by=user)
        class_2 = ClassroomFactory(name='Gravitational Mechanics', created_by=user)

        self.assertEqual(Classroom.objects.count(), 2)
        self.assertEqual(class_1.created_by, user)
        self.assertEqual(class_2.created_by, user)
        self.assertEqual(class_1.name, 'Astrophysics')
        self.assertEqual(class_2.name, 'Gravitational Mechanics')

    def test_only_the_user_who_created_a_classroom_can_edit_it(self):
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_1)
        class_3 = ClassroomFactory(created_by=user_2)

        self.assertEqual(Classroom.objects.count(), 3)
        self.assertTrue(class_1.can_edit(user_1))
        self.assertTrue(class_2.can_edit(user_1))
        self.assertTrue(class_3.can_edit(user_2))

        self.assertFalse(class_1.can_edit(user_2))
        self.assertFalse(class_2.can_edit(user_2))
        self.assertFalse(class_3.can_edit(user_1))

    def test_superuser_can_edit_any_class(self):
        super_user = get_user_model().objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='superpass123'
        )
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_2)

        self.assertTrue(class_1.can_edit(super_user))
        self.assertTrue(class_1.can_edit(user_1))
        self.assertFalse(class_1.can_edit(user_2))

        self.assertTrue(class_2.can_edit(super_user))
        self.assertFalse(class_2.can_edit(user_1))
        self.assertTrue(class_2.can_edit(user_2))

    def test_only_a_user_who_created_a_class_can_update_it(self):
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_2)

        self.assertTrue(class_1.can_update(user_1))
        self.assertFalse(class_1.can_update(user_2))

        self.assertFalse(class_2.can_update(user_1))
        self.assertTrue(class_2.can_update(user_2))

    def test_superuser_can_update_any_class(self):
        super_user = get_user_model().objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='superpass123'
        )
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_2)

        self.assertTrue(class_1.can_update(super_user))
        self.assertTrue(class_2.can_update(super_user))

    def test_only_a_user_who_created_a_class_can_delete_it(self):
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_2)

        self.assertTrue(class_1.can_delete(user_1))
        self.assertFalse(class_1.can_delete(user_2))

        self.assertFalse(class_2.can_delete(user_1))
        self.assertTrue(class_2.can_delete(user_2))

    def test_superuser_can_delete_any_class(self):
        super_user = get_user_model().objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='superpass123'
        )
        user_1 = UserFactory()
        user_2 = UserFactory()
        class_1 = ClassroomFactory(created_by=user_1)
        class_2 = ClassroomFactory(created_by=user_2)

        self.assertTrue(class_1.can_delete(super_user))
        self.assertTrue(class_2.can_delete(super_user))


class EnrollmentTests(TestCase):
    def test_enrollment_creation_between_user_and_classroom(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        classroom_1 = ClassroomFactory()
        classroom_2 = ClassroomFactory()

        enrollment_1 = EnrollmentFactory(student=user_1, classroom=classroom_1)
        enrollment_2 = EnrollmentFactory(student=user_2, classroom=classroom_2)

        self.assertEqual(Enrollment.objects.count(), 2)

        self.assertEqual(enrollment_1.student, user_1)
        self.assertEqual(enrollment_1.classroom, classroom_1)

        self.assertEqual(enrollment_2.student, user_2)
        self.assertEqual(enrollment_2.classroom, classroom_2)
