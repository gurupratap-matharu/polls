from django.urls import path

from polls.views import (QuestionCreate, QuestionDelete, QuestionDetailView,
                         QuestionListView, QuestionUpdate, ResultsView,
                         VoteView)

app_name = 'polls'
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:question>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreate.as_view(), name='question_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:question>/update/', QuestionUpdate.as_view(), name='question_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:question>/delete/', QuestionDelete.as_view(), name='question_delete'),
    path('<int:year>/<int:month>/<int:day>/<slug:question>/results/', ResultsView.as_view(), name='results'),
    path('<int:year>/<int:month>/<int:day>/<slug:question>/vote/', VoteView.as_view(), name='vote'),
]
