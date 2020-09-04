import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from classroom.forms import EnrollmentForm
from classroom.models import Classroom, Enrollment

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


class EnrollmentCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'classroom/enrollment_form.html'
    success_message = 'Great! You have enrolled successfully.'
    form_class = EnrollmentForm
    success_url = reverse_lazy('classroom_list')

    def form_valid(self, form):
        code = self.request.POST['code']
        student = self.request.user
        classroom = Classroom.objects.get(id=code)

        enrollment, created = Enrollment.objects.get_or_create(student=student, classroom=classroom)

        if not created:
            logger.info('%s already enrolled in %s! redirecting...', student, classroom.name)
            messages.info(self.request, 'You are already enrolled in {}!'.format(classroom))
            return redirect(reverse_lazy('classroom_list'))

        logger.info('Enrolled in %s', enrollment)
        form.send_mail(student=student, classroom=classroom)
        return super().form_valid(form)
