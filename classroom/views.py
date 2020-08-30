import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from classroom.models import Classroom

logger = logging.getLogger(__name__)


class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    context_object_name = 'classroom_list'
    template_name = 'classroom/classroom_list.html'


class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = Classroom
    context_object_name = 'classroom'
    template_name = 'classroom/classroom_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit(self.request.user)
        logger.info('can_edit:%s', context['can_edit'])
        return context


class ClassroomCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Classroom
    fields = ['name', 'section', 'subject', 'room']
    template_name = 'classroom/classroom_form.html'
    success_message = "%(name)s successfully created!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClassroomUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Classroom
    fields = ['name', 'section', 'subject', 'room']
    template_name = 'classroom/classroom_update_form.html'
    success_message = "%(name)s successfully updated!"


class ClassroomDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Classroom
    success_url = reverse_lazy('classroom_list')
    success_message = "%(name)s successfully deleted!"
