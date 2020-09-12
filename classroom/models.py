import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    section = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    room = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    students = models.ManyToManyField(get_user_model(), through='Enrollment', related_name='classes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classroom_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('classroom_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('classroom_delete', args=[str(self.id)])

    def can_edit(self, user):
        return user.is_superuser or self.created_by == user

    def can_update(self, user):
        return user.is_superuser or self.created_by == user

    def can_delete(self, user):
        return user.is_superuser or self.created_by == user

    def get_enrollment(self, user):
        return self.enrollment_set.get(student=user)


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='enrollments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='enrollments')
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return ", ".join(
            [
                self.classroom.name,
                self.student.email,
            ]
        )

    def get_delete_url(self):
        return reverse('enroll_delete', args=[str(self.id)])


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return self.title

    def can_update(self, user):
        return user.is_superuser or self.author == user

    def can_delete(self, user):
        return user.is_superuser or self.author == user
