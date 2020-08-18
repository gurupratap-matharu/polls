from django.urls import path

from polls.views import (QuestionDetailView, QuestionListView, ResultsView,
                         VoteView)

app_name = 'polls'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('<int:pk>/vote/', VoteView.as_view(), name='vote'),
]
