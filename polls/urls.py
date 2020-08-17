from django.urls import path

from polls.views import (HomePageView, QuestionDetailView, QuestionListView,
                         ResultsView, VoteView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('questions/<int:pk>/vote/', VoteView.as_view(), name='vote'),
]
