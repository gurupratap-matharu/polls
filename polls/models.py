import datetime
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Question(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='pub_date')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(through=UUIDTaggedItem)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('polls:question_detail', args=[self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug])

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_update_url(self):
        return reverse('polls:question_update', args=[self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug])

    def get_delete_url(self):
        return reverse('polls:question_delete', args=[self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug])

    def can_update(self, user):
        return user.is_superuser or self.created_by == user

    def can_delete(self, user):
        return user.is_superuser or self.created_by == user


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.choice_text

    def get_absolute_url(self):
        return reverse('choice_detail', args=str([self.id]))
