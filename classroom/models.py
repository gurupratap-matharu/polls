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
        return reverse('classroom', args=[str(self.id)])
