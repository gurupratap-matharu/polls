from django.forms import inlineformset_factory

from polls.models import Choice, Question

ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text'))
