from django.views.generic import ListView

from classroom.models import Classroom


class ClassroomListView(ListView):
    model = Classroom
    context_object_name = 'classroom_list'
    template_name = 'classroom/classroom_list.html'
