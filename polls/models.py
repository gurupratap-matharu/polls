import datetime
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('polls:question_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('polls:question_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('polls:question_delete', args=[str(self.id)])

    def can_update(self, user):
        return user.is_superuser or self.created_by == user

    def can_delete(self, user):
        return user.is_superuser or self.created_by == user


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    def get_absolute_url(self):
        return reverse('choice_detail', args=str([self.id]))
