from django.urls import path

from polls.views import (QuestionCreate, QuestionDelete, QuestionDetailView,
                         QuestionListView, QuestionUpdate, ResultsView,
                         VoteView)

app_name = 'polls'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<int:uuid>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreate.as_view(), name='question_create'),
    path('<int:uuid>/update/', QuestionUpdate.as_view(), name='question_update'),
    path('<int:uuid>/delete/', QuestionDelete.as_view(), name='question_delete'),
    path('<int:uuid>/results/', ResultsView.as_view(), name='results'),
    path('<int:uuid>/vote/', VoteView.as_view(), name='vote'),
]
