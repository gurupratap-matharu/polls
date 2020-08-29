from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from classroom.models import Classroom


class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    context_object_name = 'classroom_list'
    template_name = 'classroom/classroom_list.html'


class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = Classroom
    context_object_name = 'classroom'
    template_name = 'classroom/classroom_detail.html'
