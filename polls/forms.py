from django.forms import ModelForm

from polls.models import Question


class QuestionForm(ModelForm):
    model = Question


class VoteForm()
