import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import (CreateView, DeleteView, FormMixin,
                                       UpdateView)

from classroom.forms import EnrollmentForm, PostForm
from classroom.models import Classroom, Enrollment

logger = logging.getLogger(__name__)


class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    context_object_name = 'classroom_list'
    template_name = 'classroom/classroom_list.html'

    def get_queryset(self):
        return self.model.objects.filter(
            Q(students=self.request.user) | Q(created_by=self.request.user)
        ).distinct()


class ClassroomDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Classroom
    context_object_name = 'classroom'
    template_name = 'classroom/classroom_detail.html'
    success_message = "Post successfully created!"
    form_class = PostForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.classroom = self.get_object()
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, self.success_message)
        logger.info('saved post with form...%s', form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.object.can_update(self.request.user)
        context['enrollment'] = self.object.get_enrollment(self.request.user)
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

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_update(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj


class ClassroomDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Classroom
    success_url = reverse_lazy('classroom_list')
    success_message = "Classroom successfully deleted!"

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_delete(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ClassroomDelete, self).delete(request, *args, **kwargs)


class EnrollmentCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'classroom/enrollment_form.html'
    success_message = 'Great! You have enrolled successfully.'
    form_class = EnrollmentForm
    success_url = reverse_lazy('classroom_list')

    def form_valid(self, form):
        code = self.request.POST['code']
        student = self.request.user
        classroom = get_object_or_404(Classroom, id=code)

        enrollment, created = Enrollment.objects.get_or_create(student=student, classroom=classroom)

        if not created:
            logger.info('%s already enrolled in %s! redirecting...', student, classroom.name)
            messages.info(self.request, 'You are already enrolled in {}!'.format(classroom))
            return redirect(reverse_lazy('classroom_list'))

        logger.info('Enrolled in %s', enrollment)
        form.send_mail(student=student, classroom=classroom)
        return super().form_valid(form)


class EnrollmentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Enrollment
    template_name = 'classroom/enrollment_confirm_delete.html'
    success_url = reverse_lazy('classroom_list')
    success_message = "You have unenrolled successfully!"

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_delete(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EnrollmentDelete, self).delete(request, *args, **kwargs)
