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

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

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
