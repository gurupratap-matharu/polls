from django.urls import path

from polls.views import (QuestionCreate, QuestionDelete, QuestionDetailView,
                         QuestionListView, QuestionUpdate, ResultsView,
                         VoteView)

app_name = 'polls'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<uuid:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreate.as_view(), name='question_create'),
    path('<uuid:pk>/update/', QuestionUpdate.as_view(), name='question_update'),
    path('<uuid:pk>/delete/', QuestionDelete.as_view(), name='question_delete'),
    path('<uuid:pk>/results/', ResultsView.as_view(), name='results'),
    path('<uuid:pk>/vote/', VoteView.as_view(), name='vote'),
]
