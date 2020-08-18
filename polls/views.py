from django.views.generic import DetailView, ListView, TemplateView

from polls.models import Question


class QuestionListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'polls/question_list.html'


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/question_detail.html'


class VoteView(TemplateView):
    template_name = 'polls/vote.html'


class ResultsView(TemplateView):
    template_name = 'polls/results.html'
