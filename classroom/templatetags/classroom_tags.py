from classroom.models import Classroom
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_classrooms():
    return Classroom.objects.count()


@register.inclusion_tag('classroom/latest_classrooms.html')
def show_latest_classrooms(count=5):
    latest_classrooms = Classroom.objects.order_by('-created_at')[:count]
    return {'latest_classrooms': latest_classrooms}


@register.inclusion_tag('classroom/popular_classrooms.html')
def show_popular_classrooms(count=5):
    popular_classrooms = Classroom.objects.annotate(student_count=Count('students')).order_by('-student_count')[:count]
    return {'popular_classrooms': popular_classrooms}


@register.inclusion_tag('classroom/top_tags.html')
def show_top_tags(count=10):
    top_tags = Classroom.tags.most_common()[:count]
    return {'top_tags': top_tags}
