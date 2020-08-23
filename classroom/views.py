from django.views.generic import TemplateView


class ClassroomListView(TemplateView):
    template_name = 'classroom/classroom_list.html'
